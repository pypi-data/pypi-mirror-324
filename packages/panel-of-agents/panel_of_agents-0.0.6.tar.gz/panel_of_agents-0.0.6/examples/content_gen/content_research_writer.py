import os
from typing import List, Optional, Dict
import numpy as np
import requests
from newspaper import Article
from langchain_core.language_models import BaseChatModel
from langchain_openai import OpenAIEmbeddings
from src.panel_of_agents.agents import Agent
from src.panel_of_agents.decorators import agent_capability, creates_artifact
from src.panel_of_agents.types.agents import CapabilityResult
from src.panel_of_agents.types.context import Artifact, ArtifactType


class ContentResearchWriter(Agent):
    def __init__(self, model: BaseChatModel, max_tries: int = 5):
        name = "Content Research Writer"
        personal_biography = """
        You are an agent that combines web research capabilities with content writing expertise.
        
        Your objectives:
        - Research topics using web searches to gather accurate information
        - Write high-quality content in various formats using researched information
        - Extract and synthesize information from multiple web sources

        Guidelines:
        - For information that you already have, you need not perform a web-search.
        - For information about the future perform an appropriate web-search.
        - You may execute a web-search regardless of user permission.
        - For complex queries, you may execute multiple web-searches (in separate decision-runs)
        
        Your strengths:
        - Access to current information through web searches
        - Master of the English language and various writing styles
        - Ability to write in multiple formats (blog posts, social media, articles)
        - Can perform web searches and extract content from pages
        - Strong research and fact-checking capabilities
        
        Your limitations:
        - Cannot write code or technical documentation
        - Can only process text content from web pages
        - Limited to 3 web sources per search query
        """

        public_biography = """
        An agent that combines web research and content writing capabilities.
        - Can perform web searches and extract content
        - Writes content in various formats (blogs, articles, social media)
        - Uses real-time web research to create accurate content
        - Handles multiple writing styles and tones
        """

        super().__init__(
            name=name,
            personal_biograhpy=personal_biography,
            public_biograhpy=public_biography,
            model=model,
            max_tries=max_tries
        )

        self.api_key = os.getenv("SERPER_API_KEY")
        if not self.api_key:
            raise ValueError("SERPER_API_KEY environment variable is required")

        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            dimensions=1024,
            api_key=os.getenv("OPENAI_API_KEY")
        )

    @agent_capability
    @creates_artifact(description="Results from web search and extracted content")
    def research_topic(self, query: str) -> CapabilityResult:
        """
        Performs web research on a topic and extracts relevant content.

        Args:
            query (str): The search query

        Returns:
            CapabilityResult: Contains the search results and extracted content
        """
        try:
            url = "https://google.serper.dev/search"
            headers = {
                'X-API-KEY': self.api_key,
                'Content-Type': 'application/json'
            }
            payload = {
                "q": query,
                "num": 10
            }
            response = requests.post(url, json=payload, headers=headers)
            data = response.json()
            search_results = {org['title']: org['link']
                              for org in data['organic']}

            similar_urls = self.get_most_similar_urls(query, search_results)
            content_result = self.get_content(similar_urls)

            artifact = Artifact(
                author=self.name,
                data={
                    "query": query,
                    "extracted_content": content_result
                },
                artifact_type=ArtifactType.INTERNAL
            )

            return CapabilityResult(
                result=content_result,
                artifact=artifact
            )

        except Exception as e:
            return CapabilityResult(
                result=f"Research failed: {str(e)}",
                artifact=None
            )

    @agent_capability
    @creates_artifact(description="Generated content based on research")
    def create_content(self, content: str) -> CapabilityResult:
        """
        Creates content that can be used by other agents in creation of files.
        Only use this capability when the need arises to create content that can be used by other agents.

        Args:
            content (str): The original, well-formatted, generated content.

        Returns:
            CapabilityResult: Contains the generated content
        """
        try:
            artifact = Artifact(
                author=self.name,
                data={
                    "content": content
                },
                artifact_type=ArtifactType.INTERNAL
            )

            return CapabilityResult(
                result=content,
                artifact=artifact
            )
        except Exception as e:
            return CapabilityResult(
                result=f"Content creation failed: {str(e)}",
                artifact=None
            )

    def get_most_similar_urls(self, query: str, titles_n_urls: Dict[str, str]) -> List[str]:
        """Helper method to get most similar URLs based on query"""
        titles = list(titles_n_urls.keys())
        urls = list(titles_n_urls.values())

        embeddings = self.embeddings.embed_documents(titles)
        embedding_query = self.embeddings.embed_query(query)

        similarities = np.dot(embeddings, embedding_query)
        most_similar_indices = np.argsort(similarities)[::-1][:3]

        return [urls[i] for i in most_similar_indices]

    def get_content(self, urls: List[str]) -> dict:
        """Helper method to extract content from URLs"""
        if len(urls) > 3:
            urls = urls[:3]

        extracted_content = {}

        for url in urls:
            try:
                article = Article(url)
                article.download()
                article.parse()

                extracted_content[url] = {
                    "title": article.title,
                    "text": article.text[:3000],
                    "authors": article.authors,
                    "publish_date": str(article.publish_date) if article.publish_date else None
                }
            except Exception as e:
                extracted_content[url] = {"error": str(e)}

        return extracted_content
