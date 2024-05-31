import requests
import feedparser
import os
import re

# URL of the RSS feed
rss_feed_url = "https://www.omnycontent.com/d/playlist/8f7208d2-db6e-4bfa-85b5-ad3d00776f1f/cd527cc1-f690-412c-8ff4-ad440125a3ed/c26c1864-165e-4bb1-b7e8-ad440125a3f6/podcast.rss"  # Replace this with the actual RSS feed URL

# Parse the RSS feed
feed = feedparser.parse(rss_feed_url)

# Directory to save the downloaded audio files
download_directory = r"C:\Users\Derrick\podcast-audio-scrapping\Khibika Natsi"

# Create the directory if it does not exist
os.makedirs(download_directory, exist_ok=True)

# Function to sanitize the file name
def sanitize_filename(filename):
    # Remove any characters that are not alphanumeric, spaces, underscores, or hyphens
    return re.sub(r'[^a-zA-Z0-9\s_-]', '', filename).strip()

# Iterate through each item in the RSS feed
for entry in feed.entries:
    # Extract the audio URL
    enclosure = entry.get('enclosures')
    if enclosure:
        audio_url = enclosure[0].get('url')
        if audio_url:
            # Extract the title and sanitize it for use as a file name
            title = entry.get('title', 'Untitled')
            sanitized_title = sanitize_filename(title)
            
            # Add file extension
            file_name = f"{sanitized_title}.mp3"

            # Full path to save the audio file
            file_path = os.path.join(download_directory, file_name)

            # Download the audio file
            response = requests.get(audio_url, stream=True)

            # Check if the request was successful
            if response.status_code == 200:
                # Open the file in binary mode and write the content
                with open(file_path, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
                print(f"Downloaded '{file_name}' successfully.")
            else:
                print(f"Failed to download '{file_name}'. Status code: {response.status_code}")
