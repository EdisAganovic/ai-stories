#!/usr/bin/env python3
"""
Simple test to verify OpenRouter API access
"""

import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_openrouter_connection():
    """Test basic connection to OpenRouter."""
    api_key = os.environ.get("OPENROUTER_API_KEY")
    
    if not api_key:
        print("ERROR: OPENROUTER_API_KEY environment variable is not set.")
        return False

    print("Testing OpenRouter API connection...")
    
    try:
        # Configure OpenAI to use OpenRouter
        client = openai.OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        
        # Make a simple test call
        response = client.chat.completions.create(
            model="openrouter/polaris-alpha",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10
        )
        
        print("SUCCESS: API call completed successfully!")
        print(f"Response: {response.choices[0].message.content}")
        return True

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_openrouter_connection()