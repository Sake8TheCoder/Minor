import requests


def get_wikipedia_search_results(query, max_results=3):
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
        print("Error making request to Wikipedia API")
        return None


def generate_wikipedia_links(user_input, max_results=5):
    related_links = get_wikipedia_search_results(user_input, max_results)

    if related_links:
        print(f"Top {max_results} Wikipedia links related to '{user_input}':")
        for idx, link in enumerate(related_links, 1):
            print(f"{idx}. {link}")
    else:
        print(f"No results found for '{user_input}'.")
