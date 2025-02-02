from pathlib import Path
from typing import List
from langchain_core.language_models import BaseChatModel
from src.panel_of_agents.agents import Agent
from src.panel_of_agents.decorators import agent_capability
from src.panel_of_agents.types.agents import CapabilityResult


class FileManager(Agent):
    def __init__(self, model: BaseChatModel, max_tries: int = 5):
        name = "File Manager"
        personal_biography = """
        You are a File System Agent that manages files in a sandbox directory.
        You can:
        - List files in the sandbox directory
        - Create text/markdown files
        - Read content from text/markdown files
        
        Your strengths:
        - Efficient file system operations
        - Safe file handling within sandbox
        - Text and markdown file manipulation
        
        Your limitations:
        - Can only work within the 'examples/content_gen/files/' directory
        - Can only handle text and markdown files
        - Cannot modify or delete existing files
        - You DO NOT possess any knowledge about anything, you are a file manager.
        - You MUST NOT generate content for files, you can only create files based on content provided by others.
        - You DO NOT know anything about content generation, and you have an awful command of the English language.
        """

        public_biography = """
        A File System Agent that manages files in a sandbox directory.
        Capabilities:
        - List files in directory
        - Create text/markdown files
        - Read text/markdown files
        """

        super().__init__(
            name=name,
            personal_biograhpy=personal_biography,
            public_biograhpy=public_biography,
            model=model,
            max_tries=max_tries
        )

        # Ensure the files directory exists with the correct path
        self.files_dir = Path(__file__).parent / "files"
        self.files_dir.mkdir(exist_ok=True)

    @agent_capability
    def list_files(self) -> CapabilityResult:
        """Lists all files in the files directory."""
        try:
            files = [f.name for f in self.files_dir.glob("*") if f.is_file()]
            result = f"Files found: {', '.join(files) if files else 'No files found'}"
            return CapabilityResult(result=result, artifact=None)
        except Exception as e:
            return CapabilityResult(
                result=f"Error listing files: {str(e)}",
                artifact=None
            )

    @agent_capability
    def create_file(self, filename: str, content: str) -> CapabilityResult:
        """Creates a new text or markdown file with the given content."""
        try:
            # Validate file extension
            if not (filename.endswith('.txt') or filename.endswith('.md')):
                return CapabilityResult(
                    result="Error: Only .txt and .md files are supported",
                    artifact=None
                )

            # Ensure the file path is within the sandbox
            file_path = self.files_dir / filename
            if not str(file_path.resolve()).startswith(str(self.files_dir.resolve())):
                return CapabilityResult(
                    result="Error: File path must be within the files directory",
                    artifact=None
                )

            # Don't overwrite existing files
            if file_path.exists():
                return CapabilityResult(
                    result=f"Error: File {filename} already exists",
                    artifact=None
                )

            # Create the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            return CapabilityResult(
                result=f"Successfully created file: {filename}",
                artifact=None
            )
        except Exception as e:
            return CapabilityResult(
                result=f"Error creating file: {str(e)}",
                artifact=None
            )

    @agent_capability
    def read_file(self, filename: str) -> CapabilityResult:
        """Reads content from a text or markdown file."""
        try:
            # Validate file extension
            if not (filename.endswith('.txt') or filename.endswith('.md')):
                return CapabilityResult(
                    result="Error: Only .txt and .md files are supported",
                    artifact=None
                )

            # Ensure the file path is within the sandbox
            file_path = self.files_dir / filename
            if not str(file_path.resolve()).startswith(str(self.files_dir.resolve())):
                return CapabilityResult(
                    result="Error: File path must be within the files directory",
                    artifact=None
                )

            # Check if file exists
            if not file_path.exists():
                return CapabilityResult(
                    result=f"Error: File {filename} does not exist",
                    artifact=None
                )

            # Read the file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            return CapabilityResult(
                result=f"Content of {filename}:\n{content}",
                artifact=None
            )
        except Exception as e:
            return CapabilityResult(
                result=f"Error reading file: {str(e)}",
                artifact=None
            )
