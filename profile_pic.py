import requests
from bs4 import BeautifulSoup

def get_tiktok_profile_pic(username):
    url = f"https://www.tiktok.com/@{username}"
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Referer': 'https://www.tiktok.com/'
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to load profile page: {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')
    img_tag = soup.find("img", class_="css-1zpj2q-ImgAvatar e1e9er4e1")
    
    if not img_tag or not img_tag.get("src"):
        raise Exception("Profile picture not found")

    profile_pic_url = img_tag["src"]
    print("Profile pic URL:", profile_pic_url)
    return profile_pic_url

# Usage
get_tiktok_profile_pic("delightmb")
