from dotenv import load_dotenv
import os

load_dotenv()

# Application Settings
APP_SETTINGS = {
  "output_folder": "outputs",
  "logs_folder": "logs",
  "locale_dropbox_path": os.getenv('LOCALE_DROPBOX_PATH'),
}

# Model Configurations 
ai_models = [
  {
    "name": "gpt-4o-mini",
    "base_url": "https://api.openai.com/v1/chat/completions",
    "api_key": os.getenv('OPENAI_API_KEY'),
    "api_type": "openai",
    "provider": "openai"
  },
  {
    "name": "gpt-4o",
    "base_url": "https://api.openai.com/v1/chat/completions",
    "api_key": os.getenv('OPENAI_API_KEY'),
    "api_type": "openai",
    "provider": "openai"
  },
  {
    "name": "mistral-small-latest",
    "base_url": "https://api.mistral.ai/v1/chat/completions",
    "api_key": os.getenv('MISTRAL_API_KEY'),
    "api_type": "openai",
    "provider": "mistral"
  },
  {
    "name": "gemini-1.5-flash",
    "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions", 
    "api_key": os.getenv('GEMINI_API_KEY'),
    "api_type": "openai", #gemini
    "provider": "google"
  },
  {
    "name": "gemini-2.0-flash-exp",
    "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions",
    "api_key": os.getenv('GEMINI_API_KEY'),
    "api_type": "openai", #gemini
    "provider": "google"
  },
  {
    "name": "claude-3-haiku",
    "base_url": "https://api.anthropic.com/v1/messages",
    "api_key": os.getenv('ANTHROPIC_API_KEY'),
    "api_type": "anthropic",
    "provider": "anthropic"
  }
]