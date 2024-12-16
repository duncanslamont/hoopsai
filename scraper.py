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
    url = "https://www.basketball-reference.com/players/"
    # Set up headers to identify our request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # Add a small delay before making the request
        time.sleep(3)
        
        # Make the request
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Create BeautifulSoup object
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the main index list
        index_list = soup.find('ul', class_='page_index')
        
        if not index_list:
            raise ValueError("Could not find player index list on the page")
        
        # Initialize list to store player information
        players = []
        
        # Iterate through all links in the index
        for link in index_list.find_all('a'):
            # Skip letter index links (they don't have player information)
            if len(link.get('href', '')) > len('/players/x/'):
                player_info = {
                    'name': link.text.strip(),
                    'url': f"https://www.basketball-reference.com{link.get('href')}",
                    'is_active': bool(link.find('strong')),  # Check if player is in <strong> tags
                    'is_hof': '*' in link.parent.text  # Check if there's an asterisk after the name
                }
                players.append(player_info)
        
        return players
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

# Example usage:

players = fetch_player_links()
for player in players[:15]:  # Print first 5 players
    print(f"Name: {player['name']}")
    print(f"URL: {player['url']}")
    print(f"Active: {player['is_active']}")
    print(f"Hall of Fame: {player['is_hof']}")
    print("---")

