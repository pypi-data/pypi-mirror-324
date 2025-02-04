import httpx
import random
from typing import Optional, Dict, Any

class PurrBot:
    BASE_URL = "https://purrbot.site/api"

    purrbot_nsfw_tags = ["anal", "blowjob", "cum", "fuck", "pussylick", "solo", "solo_male", 
                         "threesome_fff", "threesome_ffm", "threesome_mmf", "yaoi", "yuri", "neko"]
    
    purrbot_tags = ["eevee", "holo", "icon", "kitsune", "neko", "okami", "senko", "shiro"]

    purrbot_reactions = [
        "angry", "bite", "blush", "comfy", "cry", "cuddle", "dance", "fluff",
        "hug", "kiss", "lay", "lick", "pat", "neko", "poke", "pout", "slap", 
        "smile", "tail", "tickle", "eevee"
    ]


    @staticmethod
    async def get_tags() -> Dict[str, Any]:
        """Retrieve tags and reactions for gifs under SFW, and NSFW tags separately."""
        return {
            "sfw": PurrBot.purrbot_tags + PurrBot.purrbot_reactions,
            "nsfw": PurrBot.purrbot_nsfw_tags
        }

    @staticmethod
    async def fetch_sfw_gif(reaction: Optional[str] = None, tag: Optional[str] = None) -> Dict[str, Any]:
        """
        Fetch a gif from purrbot.site based on a reaction or tag.
        
        Parameters:
        - tag: Tag to filter NSFW content (optional).
        - reaction: Reaction to filter gif content (e.g., 'angry', 'hug', etc.).
        """
        if reaction and reaction not in PurrBot.purrbot_reactions:
            return {"error": "Invalid reaction"}
        
        if not tag:
            tag = random.choice(PurrBot.purrbot_nsfw_tags)

        if tag not in PurrBot.purrbot_nsfw_tags:
            return {"error": "Invalid NSFW tag"}

        url = f"{PurrBot.BASE_URL}/img/sfw/{reaction}/gif"
        
        params = {}
        params["tag"] = tag
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                return data.get("link")
            except httpx.HTTPStatusError as e:
                print(f"HTTP error occurred: {e}")
                return {"error": "Failed to fetch GIF"}
            except (httpx.RequestError, ValueError) as e:
                print(f"Request or JSON error: {e}")
                return {"error": "Request or JSON parsing failed"}

    @staticmethod
    async def fetch_nsfw_gif(tag: Optional[str] = None) -> Dict[str, Any]:
        """
        Fetch an NSFW gif based on a tag from the NSFW tags list.
        
        Parameters:
        - tag: Tag to filter NSFW gifs (optional).
        """
        if not tag:
            tag = random.choice(PurrBot.purrbot_nsfw_tags) 

        if tag and tag not in PurrBot.purrbot_nsfw_tags:
            return {"error": "Invalid NSFW tag"}

        url = f"{PurrBot.BASE_URL}/img/nsfw/{tag}/gif"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url)
                response.raise_for_status()
                data = response.json()
                return data.get("link")
            except httpx.HTTPStatusError as e:
                print(f"HTTP error occurred: {e}")
                return {"error": "Failed to fetch NSFW GIF"}
            except (httpx.RequestError, ValueError) as e:
                print(f"Request or JSON error: {e}")
                return {"error": "Request or JSON parsing failed"}

    @staticmethod
    async def fetch_sfw_images(tag: Optional[str] = None) -> Dict[str, Any]:
        """
        Fetch an image from purrbot.site based on a tag.
        
        Parameters:
        - tag: Tag to filter content (optional).
        """
        if not tag:
            tag = random.choice(PurrBot.purrbot_tags) 
        
        if tag and tag not in PurrBot.purrbot_tags:
            return {"error": "Invalid tag"}
        
        url = f"{PurrBot.BASE_URL}/img/sfw/{tag}/img"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url)
                response.raise_for_status()
                
                data = response.json()
                return data.get("link")
            except httpx.HTTPStatusError as e:
                print(f"HTTP error occurred: {e}")
                return {"error": "Failed to fetch image"}
            except (httpx.RequestError, ValueError) as e:
                print(f"Request or JSON error: {e}")
                return {"error": "Request or JSON parsing failed"}
