import subprocess
from typing import Optional
from langchain_core.language_models import BaseChatModel
from src.panel_of_agents.agents import Agent
from src.panel_of_agents.decorators import agent_capability, creates_artifact
from src.panel_of_agents.types.agents import CapabilityResult
from src.panel_of_agents.types.context import Artifact


class CodeRunner(Agent):
    def __init__(self, model: BaseChatModel, max_tries: int = 3):
        name = "Code Runner"
        personal_biography = """
        You are an agent that can execute Python code safely in a controlled environment.
        
        Your strengths:
        - Ability to run Python code snippets
        - Can capture and return both stdout and stderr
        - Can handle basic error cases
        - Can execute code and return results
        
        Your limitations:
        - Cannot modify system files
        - Cannot install packages
        - Limited to Python code execution only
        - Must run code in a safe, controlled manner
        - MUST not create, delete or modify files using python code. This is strictly FORBIDDEN.
        """

        public_biography = """
        An agent that can execute Python code snippets and return their results.
        - Can run Python code and capture output
        - Handles execution errors gracefully
        - Returns both successful results and error messages
        """

        super().__init__(
            name=name,
            personal_biograhpy=personal_biography,
            public_biograhpy=public_biography,
            model=model,
            max_tries=max_tries
        )

    @agent_capability
    @creates_artifact(description="Result of Python code execution")
    def run_python_code(self, code: str) -> CapabilityResult:
        """
        Executes a Python code snippet and returns the result.

        Args:
            code (str): The Python code to execute

        Returns:
            CapabilityResult: Contains the execution result and any output/errors
        """
        try:
            # Create a temporary Python file
            with open("temp_code.py", "w") as f:
                f.write(code)

            # Run the code using subprocess
            result = subprocess.run(
                ["python", "temp_code.py"],
                capture_output=True,
                text=True,
                timeout=30  # 30 second timeout
            )

            # Clean up the temporary file
            subprocess.run(["rm", "temp_code.py"])

            # Prepare the output
            output = {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode
            }

            # Create an artifact with the execution results
            artifact = Artifact(
                author=self.name,
                data={
                    "code": code,
                    "execution_result": output
                }
            )

            # Return success or error message based on return code
            if result.returncode == 0:
                return CapabilityResult(
                    result=f"Code executed successfully. Output:\n{result.stdout}",
                    artifact=artifact
                )
            else:
                return CapabilityResult(
                    result=f"Code execution failed. Error:\n{result.stderr}",
                    artifact=artifact
                )

        except subprocess.TimeoutExpired:
            return CapabilityResult(
                result="Code execution timed out after 30 seconds",
                artifact=None
            )
        except Exception as e:
            return CapabilityResult(
                result=f"Error executing code: {str(e)}",
                artifact=None
            )
