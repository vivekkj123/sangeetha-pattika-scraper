import requests
from bs4 import BeautifulSoup
import urllib.parse
import difflib

# Base URL to fetch pages
BASE_URL = "https://www.malayalasangeetham.info/songs.php?singers=P%20Jayachandran&singtype=solo&tag=Search&limit=470&page_num={}"

def scrape_page(page_num):
    """
    Scrapes the specified page and extracts the song details.
    """
    url = BASE_URL.format(page_num)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    rows = soup.select('tr.ptableslist')
    page_data = []

    for row in rows:
        columns = row.find_all('td')
        if len(columns) >= 3:
            song_name = columns[0].text.strip()
            movie_name = columns[1].text.strip()
            year = columns[2].text.strip()
            page_data.append((year, movie_name, song_name))
    return page_data


import requests
import difflib

def find_wikipedia_article(movie_name):
    """
    Searches Wikipedia for a movie article based on the given movie name.
    Prioritizes:
    1. Articles ending with '_(ചലച്ചിത്രം)' with at least 75% similarity.
    2. Exact matches (case-insensitive).
    3. Fallback matches with >75% similarity from other articles.
    """
    base_url = "https://ml.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": movie_name,
        "format": "json",
    }

    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        return None

    search_results = response.json().get("query", {}).get("search", [])
    if not search_results:
        return None

    # Normalize movie name for comparison
    normalized_movie_name = movie_name.strip().lower()

    # 1. Filter articles ending with '_(ചലച്ചിത്രം)'
    suffix_results = [result for result in search_results if result["title"].endswith("(ചലച്ചിത്രം)")]

    # Check for exact match among suffix results
    for result in suffix_results:
        if result["title"].strip().lower() == normalized_movie_name + " (ചലച്ചിത്രം)":
            return result["title"]

    # Check for >75% similarity among suffix results
    best_suffix_match = None
    highest_suffix_similarity = 0
    for result in suffix_results:
        similarity = difflib.SequenceMatcher(None, movie_name, result["title"]).ratio()
        if similarity > 0.75 and similarity > highest_suffix_similarity:
            best_suffix_match = result["title"]
            highest_suffix_similarity = similarity

    if best_suffix_match:
        return best_suffix_match

    # 2. Check for exact matches among all results (case-insensitive)
    exact_match = next(
        (result["title"] for result in search_results if result["title"].strip().lower() == normalized_movie_name),
        None,
    )
    if exact_match:
        return exact_match

    # 3. Fallback: Check similarity for other results
    best_match = None
    highest_similarity = 0
    for result in search_results:
        title = result["title"]
        similarity = difflib.SequenceMatcher(None, movie_name, title).ratio()
        if similarity > 0.75 and similarity > highest_similarity:  # Ensure similarity > 75%
            best_match = title
            highest_similarity = similarity

    return best_match

def generate_wikipedia_table_with_links(data):
    """
    Converts the extracted data into a Wikipedia table with rowspan for both years and movies.
    Adds links to Wikipedia articles for movies.
    Removes quotes from the song names.
    """
    grouped_data = {}
    for year, movie, song in data:
        if year not in grouped_data:
            grouped_data[year] = {}
        if movie not in grouped_data[year]:
            grouped_data[year][movie] = []
        grouped_data[year][movie].append(song)

    sorted_years = sorted(grouped_data.keys())

    wikipedia_table = (
        "{| class=\"wikitable\"\n"
        "|- style=\"background:#ccc; text-align:center;\"\n"
        "! Year \n! Film !! Song\n"
    )

    for year in sorted_years:
        movies = grouped_data[year]
        year_rowspan = sum(len(songs) for songs in movies.values())
        first_movie = True

        for movie, songs in movies.items():
            movie_rowspan = len(songs)
            # Find Wikipedia article for the movie
            article_title = find_wikipedia_article(movie)
            if article_title:
                movie_link = f"[[{article_title}|{movie}]]"
            else:
                movie_link = f"''{movie}''"

            for idx, song in enumerate(songs):
                wikipedia_table += "|-\n"
                if first_movie and idx == 0:
                    wikipedia_table += f"| rowspan=\"{year_rowspan}\" | {year} \n"
                    wikipedia_table += f"| rowspan=\"{movie_rowspan}\" | {movie_link} \n"
                elif idx == 0:
                    wikipedia_table += f"| rowspan=\"{movie_rowspan}\" | {movie_link} \n"
                wikipedia_table += f"| {song}\n"

            first_movie = False

    wikipedia_table += "|}\n"
    # Add the reference citation at the end
    wikipedia_table += "{{cite web |url=https://www.malayalasangeetham.info/ |title=Malayalasangeetham.info |website=Malayalasangeetham |access-date={{CURRENTMONTHNAME}} {{CURRENTDAY}}, {{CURRENTYEAR}} }}\n"
    return wikipedia_table



def main():
    all_data = []
    total_pages = 10  # Adjust this if there are more pages

    for page_num in range(1, total_pages + 1):
        print(f"Scraping page {page_num}...")
        page_data = scrape_page(page_num)
        all_data.extend(page_data)

    print("Generating Wikipedia table...")
    wikipedia_table = generate_wikipedia_table_with_links(all_data)

    # Save the output to a text file
    output_path = "songs_wikipedia_table.txt"
    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(wikipedia_table)

    print(f"Wikipedia table has been saved to {output_path}")

if __name__ == "__main__":
    main()
