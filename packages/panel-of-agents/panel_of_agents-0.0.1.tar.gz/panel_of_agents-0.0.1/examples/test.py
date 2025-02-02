import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

from .content_gen.file_manager import FileManager
from .content_gen.code_runner import CodeRunner


load_dotenv()

file_manager = FileManager(model=ChatOpenAI(model_name="gpt-4o-mini"))

file_manager.list_files()

print(file_manager.read_file("test_file.txt"))
