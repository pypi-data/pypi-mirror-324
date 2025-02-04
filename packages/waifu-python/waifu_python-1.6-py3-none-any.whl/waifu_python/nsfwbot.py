import httpx
import random
from typing import Dict, Any, Optional

class NSFWBot:
    BASE_URL = "https://api.n-sfw.com"

    @staticmethod
    async def get_tags() -> Dict[str, Any]:
        """Fetch available SFW and NSFW tags."""
        url = f"{NSFWBot.BASE_URL}/endpoints"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()
                return response.json() 
        except Exception as e:
            print(f"Error fetching tags: {e}")
            return {"error": str(e)}
    
    @staticmethod
    async def _fetch_image(endpoint_type: str, tag: str) -> Optional[str]:
        """Fetch image and return only the 'url_cdn' value."""
        url = f"{NSFWBot.BASE_URL}/{endpoint_type}/{tag.lower()}"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()
                data = response.json()
                return data.get("url_cdn")  
        except httpx.HTTPStatusError as e:
            print(f"HTTP error ({e.response.status_code}): {e}")
        except Exception as e:
            print(f"error: {e}")
        
        return None 

    @staticmethod
    async def fetch_sfw_images(tag: Optional[str] = None) -> Dict[str, Any]:
        """Fetch an SFW image. If no tag is provided, select a random SFW tag."""
        tags = await NSFWBot.get_tags()
        if "sfw" not in tags or not tags["sfw"]:
            return {"error": "No available SFW tags."}

        tag = tag or random.choice(tags["sfw"])
        return await NSFWBot._fetch_image("sfw", tag)

    @staticmethod
    async def fetch_nsfw_images(tag: Optional[str] = None) -> Dict[str, Any]:
        """Fetch an NSFW image. If no tag is provided, select a random NSFW tag."""
        tags = await NSFWBot.get_tags()
        if "nsfw" not in tags or not tags["nsfw"]:
            return {"error": "No available NSFW tags."}

        tag = tag or random.choice(tags["nsfw"])
        return await NSFWBot._fetch_image("nsfw", tag)
