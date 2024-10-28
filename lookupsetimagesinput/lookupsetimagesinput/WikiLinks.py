import requests
from bs4 import BeautifulSoup
import re
import math
from concurrent.futures import ThreadPoolExecutor, as_completed

# Function to get Wikipedia search results
def get_wikipedia_search_results(query, max_results = 20):
    search_url = "https://en.wikipedia.org/w/api.php"

    params = {
        'action': 'query',
        'list': 'search',
        'srsearch': query,
        'format': 'json',
        'srlimit': max_results
    }

    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()  # Raise an error if the request failed

        data = response.json()

        # Check if the 'query' and 'search' keys are present in the response
        if 'query' in data and 'search' in data['query']:
            search_results = data['query']['search']

            related_links = []
            base_url = "https://en.wikipedia.org/wiki/"

            for result in search_results:
                title = result['title'].replace(' ', '_')  # Format title for Wikipedia URL
                link = base_url + title
                related_links.append(link)
            return related_links
        else:
            print("No search results found.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error making request to Wikipedia API: {e}")
        return None


# Function to fetch word count and keyword matches from a Wikipedia page
def get_word_count_and_keyword_matches(url, keyword):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        paragraphs = soup.find_all('p')  # Fetch paragraphs only
        text_content = ' '.join([para.get_text() for para in paragraphs])
        cleaned_text = text_content.strip()
        word_count = len(cleaned_text.split())
        #Find keyword matches (case insensitive)

        keyword_matches = len(re.findall(r'\b' + re.escape(keyword) + r's?\b', cleaned_text, flags=re.IGNORECASE))

        return word_count, keyword_matches
    except Exception as e:
        print(f"Error processing {url}: {e}")
        return 0, 0  # Return 0 in case of an error

def analyze_link(link, keyword):
    word_count, keyword_matches = get_word_count_and_keyword_matches(link, keyword)
    if keyword_matches > 0:
        score = keyword_matches * math.log(word_count) if word_count > 0 else 0
    else:
        score = 0
    return score, link

# Function to generate Wikipedia links and analyze them
def generate_wikipedia_links(user_input, max_results = 20):
    related_links = get_wikipedia_search_results(user_input, max_results)

    if related_links:
        results = []  # List to store results for sorting
        allLinks = [related_links[0]]
        related_links.remove(related_links[0])
        with ThreadPoolExecutor() as executor:
            future_to_link = {executor.submit(analyze_link, link, user_input): link for link in related_links}
            for future in as_completed(future_to_link):
                score, link = future.result()
                results.append((score, link))

        results = sorted(results,reverse=True)
        for score,link in results[0:2]:
         allLinks.append(link)
        return allLinks
    else:
        print(f"No results found for '{user_input}'.")

