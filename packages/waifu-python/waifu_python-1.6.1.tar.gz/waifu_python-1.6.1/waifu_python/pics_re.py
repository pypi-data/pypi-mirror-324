import httpx
from typing import Optional, List, Dict, Any

class PicRe:
    BASE_URL = "https://pic.re/"

    @staticmethod
    async def get_tags() -> Dict[str, Any]:
        """Fetch available tags from pic.re API."""
        url = f"{PicRe.BASE_URL}tags"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                return response.json()
            raise Exception(f"Failed to fetch tags: {response.text}")

    
    @staticmethod
    async def fetch_sfw_images(tags: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Fetch image metadata from pic.re API with optional tag filtering
        
        Parameters:
        - tags: List of tags to include (e.g., ['long_hair', 'blonde_hair'])
        
        """
        params = {}
        
        if tags:
            params["in"] = ",".join(tags)
        
        url = f"{PicRe.BASE_URL}image.json"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                return data.get("file_url")
                
            except httpx.HTTPStatusError as e:
                print(f"HTTP error occurred: {e}")
                return {}
            except (httpx.RequestError, ValueError) as e:
                print(f"Request or JSON error: {e}")
                return {}