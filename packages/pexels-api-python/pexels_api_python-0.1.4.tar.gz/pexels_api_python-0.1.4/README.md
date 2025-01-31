# Pexels API Python

A Python wrapper for the Pexels API, allowing you to search for photos, get photo details, and fetch popular photos.

## Get your API KEY 

https://www.pexels.com/api/

## Installation

You can install the library using pip:

```bash
pip install pexels_api_python
```
Include the below code in your main.py

```bash
from pexels_api_python.pexels_api import PexelsAPI

# Initialize the API with your API key
api_key = "API_KEY" ENTER YOUR API KEY
pexels = PexelsAPI(api_key)

# Search for photos
search_results = pexels.search_photos("mountains")

# Download the first photo from the search results

if search_results.get("photos"):
    first_photo = search_results["photos"][0]
    photo_url = first_photo["src"]["original"]
    pexels.download_photo(photo_url, "mountains.jpg")