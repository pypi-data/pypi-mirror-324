import httpx, random

class WaifuPics:
    BASE_URL = "https://api.waifu.pics"

    @staticmethod
    async def get_tags():
        """Fetches all available tags from the /endpoints API."""
        url = f"{WaifuPics.BASE_URL}/endpoints"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                data = response.json()
                return data 
            return None

    @staticmethod
    async def fetch_sfw_images(tag=None, type="sfw"):
        """Fetches a random image from waifu.pics based on the given tag and type."""
        type = type.lower()  
        tags = await WaifuPics.get_tags()
        
        if tags is None or type not in tags:
            return None  

        tag = tag or random.choice(tags[type]) if tags[type] else None
        if not tag:
            return None  

        url = f"{WaifuPics.BASE_URL}/{type}/{tag}"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                data = response.json()
                return data["url"]
            return None

    @staticmethod
    async def fetch_nsfw_images(tag=None, type="nsfw"):
        """Fetches a random image from waifu.pics based on the given tag and type."""
        type = type.lower()  
        tags = await WaifuPics.get_tags()
        
        if tags is None or type not in tags:
            return None 

        tag = tag or random.choice(tags[type]) if tags[type] else None
        if not tag:
            return None

        url = f"{WaifuPics.BASE_URL}/{type}/{tag}"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                data = response.json()
                if "url" in data:
                    return data["url"]
            return None
