#!/usr/bin/env python3
"""
Full test of the story generation process to identify where errors occur
"""

import os
import base64
from dotenv import load_dotenv
from story_generator import get_story_prompt, generate_story_with_gemini

# Load environment variables
load_dotenv()

def test_story_generation():
    """Test the complete story generation process."""
    api_key = os.environ.get("OPENROUTER_API_KEY")
    
    if not api_key:
        print("ERROR: OPENROUTER_API_KEY environment variable is not set.")
        return False

    print("Testing complete story generation process...")
    
    # Create a minimal test image (a 1x1 pixel PNG)
    # This is the smallest valid PNG image
    test_image_data = base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
    )
    
    # Write the test image to a temporary file
    test_image_path = "temp_test_image.png"
    with open(test_image_path, "wb") as f:
        f.write(test_image_data)
    
    try:
        # Test the story generation function
        story = generate_story_with_gemini(
            image_path=test_image_path,
            child_name="Test Child",
            style="fairy tale",
            length="short"
        )
        
        print(f"SUCCESS: Story generated successfully!")
        print(f"Story preview: {story[:100]}...")
        return True
        
    except Exception as e:
        print(f"ERROR during story generation: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Clean up the temporary file
        if os.path.exists(test_image_path):
            os.remove(test_image_path)

if __name__ == "__main__":
    test_story_generation()