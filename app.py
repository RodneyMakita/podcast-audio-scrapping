import requests
from bs4 import BeautifulSoup
import os

# URL of the website to scrape
url = 'https://omny.fm/shows/ligwalagwala-drama-ngalutfota-lolumanti'

# Send a request to the website
response = requests.get(url)
html_content = response.content

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Directory to save the downloaded audio files
download_dir = r'C:\Users\Derrick\podcast-audio-scrapping\Ligwalagwala Drama Ngalutfota Lolumanti'

# Ensure the directory exists
os.makedirs(download_dir, exist_ok=True)

# Function to check if the "Load more" button is present
def load_more_present(soup):
    load_more_button = soup.find('button', class_='css-emikmj efvlbge0')
    return load_more_button is not None

# Function to click the "Load more" button
def click_load_more(session, url):
    response = session.get(url)
    return response.content

# Main scraping logic
with requests.Session() as session:
    while True:
        # Check if the "Load more" button is present
        if load_more_present(soup):
            # Click the "Load more" button
            html_content = click_load_more(session, url)
            soup = BeautifulSoup(html_content, 'html.parser')
        else:
            break

    # Find all <li> tags with the class "css-1h0a9xs"
    li_tags = soup.find_all('li', class_='css-1h0a9xs')

    # Iterate over each <li> tag and process the download links
    for li_tag in li_tags:
        # Extract the href attribute from the <a> tag within the <li> tag
        a_tag = li_tag.find('a', class_='omny-unique-0 css-lpgc1n')
        podcast_page_url = 'https://omny.fm' + a_tag['href']
        
        # Send a request to the podcast page URL
        podcast_page_response = session.get(podcast_page_url)
        podcast_page_content = podcast_page_response.content
        
        # Parse the podcast page HTML content
        podcast_page_soup = BeautifulSoup(podcast_page_content, 'html.parser')
        
        # Find all download button <a> tags with the class "css-1dx4ds5"
        download_buttons = podcast_page_soup.find_all('a', class_='css-1dx4ds5')
        
        # Extract the title from the podcast page URL
        title = podcast_page_url.split('/')[-1]
        
        for download_button in download_buttons:
            if download_button:
                # Extract the href attribute (URL of the audio file)
                audio_url = download_button['href']
                
                # Define the file path using the title and episode index
                audio_file_path = os.path.join(download_dir, f"{title}.mp3")
                
                # Save the audio file locally
                with open(audio_file_path, 'wb') as audio_file:
                    audio_file.write(session.get(audio_url).content)
                
                print(f"Podcast audio downloaded and saved to {audio_file_path}")
            else:
                print(f"No download button found for podcast page: {podcast_page_url}")
