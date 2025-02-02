from typing import List, Optional

async def vectorize_string(
    string: str,
    prompts: List[str],
    api_key: str,
    model: str,
    temperature: Optional[float] = None,
    seed: Optional[int] = None,
    base_url: Optional[str] = None
) -> List[float]:
    """
    Vectorizes a text string using concurrent processing

    Args:
        string: The input text to vectorize
        prompts: List of prompts to use for vectorization
        api_key: API key
        model: Name of the model to use
        temperature: Optional temperature setting for the model
        seed: Optional seed for random number generation
        base_url: Optional custom API base URL

    Returns:
        Vector of floats representing the vectorized text
    """
    ...

async def vectorize_image(
    image_bytes: bytes,
    prompts: List[str],
    model: str,
    api_key: str,
    temperature: Optional[float] = None,
    seed: Optional[int] = None,
    base_url: Optional[str] = None
) -> List[float]:
    """
    Vectorizes an image using concurrent processing

    Args:
        image_bytes: Raw bytes of the image to vectorize
        prompts: List of prompts to use for vectorization 
        model: Name of the model to use
        api_key: API key
        temperature: Optional temperature setting for the model
        seed: Optional seed for random number generation
        base_url: Optional custom API base URL

    Returns:
        Vector of floats representing the vectorized image
    """
    ...
