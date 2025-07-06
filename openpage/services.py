import openai
from django.conf import settings
from django.core.files.base import ContentFile
import requests # For fetching the image from URL

def generate_image_from_prompt(prompt: str):
    """
    Generates an image using OpenAI's DALL-E API based on a text prompt.

    Args:
        prompt (str): The text prompt to generate the image from.

    Returns:
        ContentFile or None: A ContentFile object containing the image data
                             if successful, None otherwise.
    """
    if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == "YOUR_OPENAI_API_KEY_HERE":
        # Consider logging this issue
        print("Error: OpenAI API key is not configured.")
        return None

    try:
        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.images.generate(
            model="dall-e-3",  # Or "dall-e-2" if preferred / for different pricing
            prompt=prompt,
            n=1,  # Number of images to generate
            size="1024x1024",  # Available sizes depend on the model (e.g., 1024x1024, 512x512, 256x256 for DALL-E 2)
            response_format="url"  # We'll get a URL to the image
        )

        if response.data and response.data[0].url:
            image_url = response.data[0].url

            # Fetch the image from the URL
            image_response = requests.get(image_url, stream=True)
            image_response.raise_for_status() # Raise an exception for HTTP errors

            # Create a Django ContentFile
            # We need a name for the file. Let's generate a simple one.
            # A more robust solution might involve generating a unique name or using part of the prompt.
            file_name = f"{prompt[:20].replace(' ', '_')}_dalle.png"
            image_content = ContentFile(image_response.content, name=file_name)
            return image_content
        else:
            # Log error: No image data in response
            print("Error: No image data received from OpenAI.")
            return None

    except openai.APIError as e:
        # Handle API errors (e.g., rate limits, server issues)
        print(f"OpenAI API Error: {e}")
        return None
    except requests.RequestException as e:
        # Handle errors in fetching the image from the URL
        print(f"Error fetching image from URL: {e}")
        return None
    except Exception as e:
        # Handle other unexpected errors
        print(f"An unexpected error occurred: {e}")
        return None
