import requests
import os

class PexelsAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.pexels.com/v1"

    def search_photos(self, query, per_page=15, page=1):
        """
        Search for photos on Pexels.

        :param query: Search query string.
        :param per_page: Number of results per page (default is 15).
        :param page: Page number to fetch (default is 1).
        :return: JSON response containing the search results.
        """
        headers = {
            "Authorization": self.api_key
        }
        params = {
            "query": query,
            "per_page": per_page,
            "page": page
        }
        response = requests.get(f"{self.base_url}/search", headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()

    def get_photo(self, photo_id):
        """
        Get details of a specific photo by its ID.

        :param photo_id: The ID of the photo.
        :return: JSON response containing the photo details.
        """
        headers = {
            "Authorization": self.api_key
        }
        response = requests.get(f"{self.base_url}/photos/{photo_id}", headers=headers)
        response.raise_for_status()
        return response.json()

    def get_popular_photos(self, per_page=15, page=1):
        """
        Get popular photos from Pexels.

        :param per_page: Number of results per page (default is 15).
        :param page: Page number to fetch (default is 1).
        :return: JSON response containing the popular photos.
        """
        headers = {
            "Authorization": self.api_key
        }
        params = {
            "per_page": per_page,
            "page": page
        }
        response = requests.get(f"{self.base_url}/popular", headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def download_photo(self, photo_url, save_path):
        """
        Download a photo from Pexels and save it to the local system.

        :param photo_url: The URL of the photo to download.
        :param save_path: The local file path where the photo will be saved.
        :return: None
        """
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(save_path), exist_ok=True)

            # Download the photo
            response = requests.get(photo_url)
            response.raise_for_status()

            # Save the photo to the specified path
            with open(save_path, "wb") as file:
                file.write(response.content)
            print(f"Photo saved to {save_path}")
        except Exception as e:
            print(f"Failed to download photo: {e}")

# Example usage:
if __name__ == "__main__":
    # Replace 'your_api_key' with your actual Pexels API key
    api_key = "your_api_key"
    pexels = PexelsAPI(api_key)

    # Search for photos
    search_results = pexels.search_photos("nature")
    print(search_results)

    # Download the first photo from the search results
    if search_results.get("photos"):
        first_photo = search_results["photos"][0]
        photo_url = first_photo["src"]["original"]  # Get the original size URL
        save_path = "downloaded_photo.jpg"  # Save to the current directory
        pexels.download_photo(photo_url, save_path)