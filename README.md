# Podcast Audio Scraper

This repository contains Python scripts to scrape audio files from various RSS feeds and save them locally. Each script is designed to parse an RSS feed, extract audio URLs, and download the audio files, renaming them based on their titles in the RSS feed.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Scripts](#scripts)
- [License](#license)

## Installation

1. **Clone the Repository:**

   ```sh
   git clone https://github.com/yourusername/podcast-audio-scraper.git
   cd podcast-audio-scraper

2. **Create a Virtual Environment:**

    ```python
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the Required Packages:**

    ```python
    pip install -r requirements.txt
    ```

 ## Usage
 
**Set Up Download Directory:**

Ensure that the directory specified in the scripts exists or will be created. Modify the download_directory variable in each script as needed.

**Run a Script:**

To run a script, use the following command:

```python
python script_name.py
Replace script_name.py with the actual name of the script you want to run.
```

Scripts
Each script is named according to the RSS feed it scrapes. The general structure of each script is as follows:

**Parse the RSS Feed:**

Each script parses the given RSS feed URL using the feedparser library.

**Extract Audio URLs and Titles:**

The script extracts audio URLs and titles from the RSS feed entries.

**Download and Save Audio Files:**

The script downloads each audio file and saves it locally with a name derived from the title.

**Here is an example of what a script looks like:**

```python
import requests
import feedparser
import os
import re

# URL of the RSS feed
rss_feed_url = "http://iono.fm/e/700081"  # Replace this with the actual RSS feed URL

# Parse the RSS feed
feed = feedparser.parse(rss_feed_url)

# Directory to save the downloaded audio files
download_directory = r"C:\Users\Derrick\podcast-audio-scrapping\Ligwalagwala Drama Ngalutfota Lolumanti"

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
```
License
This project is licensed under the MIT License. See the LICENSE file for more details.



### Additional Steps

1. **Add a `requirements.txt` File:**

   Create a `requirements.txt` file to specify the dependencies:

```txt
requests
feedparser


