import os
import asyncio
from bhumi.client import OpenAIClient

# API key and model
API_KEY = "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"
MODEL = "gpt-4o"

async def test_openai():
    """Test OpenAI client with a simple prompt"""
    print("\n🚀 Testing OpenAI client...")
    
    # Initialize client with debug mode
    client = OpenAIClient(
        max_concurrent=1,
        model=MODEL,
        debug=True
    )
    
    # Simple test prompt
    prompt = "Write a haiku about coding"
    
    # Send request
    response = await client.acompletion(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        api_key=API_KEY
    )
    
    print("\n✨ Response:")
    print(response.text)

if __name__ == "__main__":
    asyncio.run(test_openai()) 