# TikTokLiveListener

Windows

1. clone repo and cd into folder with command prompt
2. python -m venv venv
3. .\venv\Scripts\activate.bat
4. pip install TikTokLive
5. python listener.py

New Ubuntu Server

sudo apt-get update
sudo apt-get install -y \
  python3 python3-pip \
  libnss3 libxss1 libatk-bridge2.0-0 libgtk-3-0 \
  libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 libgbm1 \
  libasound2 libatk1.0-0 libcups2 libdbus-1-3 libdrm2
sudo pip3 install TikTokLive requests playwright
sudo python3 -m playwright install
python3 tiktok_live.py
python3 get_profile_pic.py
