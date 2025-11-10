#!/usr/bin/env python3
"""
Debug script to check if environment variables are loaded correctly
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

print("Environment Variables Debug:")
print("="*40)

# Check if OPENROUTER_API_KEY is loaded
api_key = os.environ.get("OPENROUTER_API_KEY")
print(f"OPENROUTER_API_KEY loaded: {api_key is not None}")
if api_key:
    # Print just the beginning and end of the key for security
    if len(api_key) > 10:
        masked_key = api_key[:6] + "..." + api_key[-4:]
        print(f"API Key (masked): {masked_key}")
    else:
        print("API Key is too short")

print(f"Full environment variable check:")
print(f"OPENROUTER_API_KEY: {'SET' if os.environ.get('OPENROUTER_API_KEY') else 'NOT SET'}")

# Check if .env file exists
import pathlib
env_path = pathlib.Path('.env')
print(f"\n.env file exists: {env_path.exists()}")

if env_path.exists():
    with open('.env', 'r') as f:
        print(f"\nContent of .env file:")
        print(f.read())