from pydantic_ai.models.groq import GroqModel
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.models.anthropic import AnthropicModel

#OPENAI_MODEL = OpenAIModel('')

#GROC_MODEL = GroqModel('deepseek-r1-distill-llama-70b')

#GEMINI_MODEL = GeminiModel('gemini-2.0-flash-exp')

#ANTHROPIC_MODEL = AnthropicModel('claude-3-5-sonnet-20241022')


from dotenv import load_dotenv
import os
#from pydantic_ai.models.openai import OpenAIModel

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Ensure the API key is available
if not OPENAI_API_KEY:
    raise ValueError("Missing OpenAI API Key. Make sure you have set it in the .env file.")

# Initialize the OpenAI model with the API key
OPENAI_MODEL = OpenAIModel('gpt-4o', api_key=OPENAI_API_KEY)
