import asyncio
import pytest
from dim_python import vectorize_string, vectorize_image
from PIL import Image
import io

# You might want to load these from environment variables in practice
BASE_URL = "http://192.168.0.101:11434/v1"
API_KEY = "sk-1234"
MODEL = "minicpm-v"  # or whatever model you're using

@pytest.mark.asyncio
async def test_vectorize_string():
    text = "This is a test string"
    prompts = [
        "What is the sentiment of this text? respond in json. example: {'score': your score in float between 0-1}",
        "What is the main topic of this text? respond in json. example: {'score': your score in float between 0-1}"
    ]
    
    result = await vectorize_string(
        string=text,
        prompts=prompts,
        model=MODEL,
        api_key=API_KEY,
        base_url=BASE_URL,
        temperature=0.0,
        seed=42
    )
    
    assert isinstance(result, list)
    assert all(isinstance(x, float) for x in result)
    assert len(result) > 0

@pytest.mark.asyncio
async def test_vectorize_image():
    # Create a simple test image
    img = Image.new('RGB', (100, 100), color='red')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    prompts = [
        "What is the brightness level of the primary color in this image? Respond in JSON. Example: {'score': your score in float between 0-1}",
        "Describe the darkness level of the primary color in this image. Respond in JSON. Example: {'score': your score in float between 0-1}"
    ]
    
    result = await vectorize_image(
        image_bytes=img_byte_arr,
        prompts=prompts,
        model=MODEL,
        api_key=API_KEY,
        base_url=BASE_URL,
        temperature=0.0,
        seed=42
    )
    
    assert isinstance(result, list)
    assert all(isinstance(x, float) for x in result)
    assert len(result) > 0

def test_missing_api_key():
    with pytest.raises(Exception):
        asyncio.run(vectorize_string(
            string="test",
            prompts=["test"],
            model=MODEL,
            api_key="",
            temperature=0.0,
            seed=42,
        ))

if __name__ == "__main__":
    pytest.main([__file__])
