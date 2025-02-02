import os
import requests
import numpy as np
from typing import List, Optional, Dict
from newspaper import Article
from langchain_core.language_models import BaseChatModel
from langchain_openai import OpenAIEmbeddings
from src.panel_of_agents.agents import Agent
from src.panel_of_agents.decorators import agent_capability, creates_artifact
from src.panel_of_agents.types.agents import CapabilityResult
from src.panel_of_agents.types.context import Artifact, ArtifactType


class WebSearchAgent(Agent):
    def __init__(self, model: BaseChatModel, max_tries: int = 5):
        name = "Web Search Agent"
        personal_biography = """
        You are an agent that can perform web searches using a Search API and extract content from web pages.

        Your objectives:
        - Answer questions using the web for information you do not inherently know.
        - Answer questions about recent information you were never trained on.
        - Extract information from web pages for other agents to use in order to generate content.

        Guidelines:
        - No need to perform a search for information that you already know.
        - No need to ask the user for comfirmation if you deem a search is necessary.
        
        Your strengths:
        - Access to information beyond your training data
        - Complete access to information from the past, present and future through the web
        - Can perform web searches and get relevant results
        - Can extract readable content from web pages
        
        Your limitations:
        - You can answer questions, you are not good at generating content for reports or other documents.
        - You can provided detailed response as you don't know how to articulate your thoughts.
        - Can only process text content from web pages
        """

        public_biography = """
        An agent that performs web searches and extracts content from web pages.
        - Uses Web Search API for web searches
        - Can extract readable content from up to 3 URLs
        - Creates structured artifacts from search results
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
    @creates_artifact(description="Results from Brave web search and extracted content")
    def get_search_results(self, query: str) -> CapabilityResult:
        """
        Performs a web search using Search API and extracts content from the most relevant URLs.

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

            # Get the most similar URLs
            similar_urls = self.get_most_similar_urls(query, search_results)

            # Extract content from the similar URLs
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
                artifact=artifact,
            )

        except requests.RequestException as e:
            return CapabilityResult(
                result=f"Search failed: {str(e)}",
                artifact=None
            )

    def get_most_similar_urls(self, query: str, titles_n_urls: Dict[str, str]) -> List[str]:
        """
        Get the most similar URLs based on the query and the titles.
        """
        titles = list(titles_n_urls.keys())
        urls = list(titles_n_urls.values())

        embeddings = self.embeddings.embed_documents(titles)
        embedding_query = self.embeddings.embed_query(query)

        similarities = np.dot(embeddings, embedding_query)
        # Return the top 3 most similar indices
        most_similar_indices = np.argsort(similarities)[::-1][:3]

        return [urls[i] for i in most_similar_indices]

    def get_content(self, urls: List[str]) -> CapabilityResult:
        """
        Extracts content from provided URLs using Newspaper3k.

        Args:
            urls (List[str]): List of URLs to extract content from (max 3)

        Returns:
            CapabilityResult: Contains the extracted content
        """
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
                extracted_content[url] = {"error": "N/A"}

        return extracted_content
