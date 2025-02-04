import httpx, random
from typing import Optional, Dict, Any

class WaifuIm:
    BASE_URL = "https://api.waifu.im/"

    @staticmethod
    async def fetch_image(tag: Optional[str] = None) -> Optional[str]:
        """Fetch an image from waifu.im API and return the direct image URL."""
        params = {}
        if tag:
            params["included_tags"] = tag
    
        url = f"{WaifuIm.BASE_URL}search"
    
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                images = data.get("images", [])
                if images:
                    return images[0].get("url") 
            raise Exception(f"Failed to fetch image: {response.text}")

    @staticmethod
    async def get_tags() -> Dict[str, Any]:
        """Fetch available tags from waifu.im API."""
        url = f"{WaifuIm.BASE_URL}tags"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                return response.json()
            raise Exception(f"Failed to fetch tags: {response.text}")

    @staticmethod
    async def fetch_sfw_images(tag: Optional[str] = None) -> Dict[str, Any]:
        """Fetch an SFW image from waifu.im API."""
        tags = await WaifuIm.get_tags()
        if "versatile" not in tags:
            return None 

        tag = tag or random.choice(tags["versatile"])

        return await WaifuIm.fetch_image(tag)

    @staticmethod
    async def fetch_nsfw_images(tag: Optional[str] = None) -> Dict[str, Any]:
        """Fetch a NSFW image from waifu.im API."""
        tags = await WaifuIm.get_tags()
        if "nsfw" not in tags:
            return None  

        tag = tag or random.choice(tags["nsfw"])

        return await WaifuIm.fetch_image(tag)
