from string import ascii_lowercase
import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import time

def fetch_player_links() -> List[Dict[str, str]]:
    """
    Fetch and extract all player links from basketball-reference players index.
    
    Args:
        url (str): URL of the basketball-reference players index
        
    Returns:
        List[Dict[str, str]]: List of dictionaries containing player names and their URLs
    """
    base_url = "https://www.basketball-reference.com/players/"
    letter_urls = []

    for c in ascii_lowercase:
        letter_urls.append(base_url + c + "/")
     # Set up headers to identify our request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    player_urls = []

    try:
        # Add a small delay before making the request
        
        for letter_url in letter_urls:
            time.sleep(4)
            response = requests.get(letter_url, headers=headers)
            response.raise_for_status()  # Raise an exception for bad status codes
        
        # Create BeautifulSoup object
            soup = BeautifulSoup(response.text, 'html.parser')
            
            players = soup.find_all('th', attrs={'scope': 'row', 'class': 'left', 'data-stat': 'player'})

    # Method 2: Using CSS selector
            players = soup.select('th[data-stat="player"]')

            for player in players:
                raw_link = str(player.find_all('a',href=True)).split("\">")[0][11:]
                link = "https://www.basketball-reference.com/" + raw_link
                player_urls.append(link)
                print(link)
                #link = player.find('a')['href']
                #link = player.find('a')['href']
    #        print(f"Name: {name}, Link: {link}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []
    with open('player_urls.txt', 'w') as f:
        for line in player_urls:
            f.write(f"{line}\n")




fetch_player_links()
