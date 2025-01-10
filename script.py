import requests
from bs4 import BeautifulSoup

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

def generate_wikipedia_table_with_rowspan(data):
    """
    Converts the extracted data into a Wikipedia table with rowspan for both years and movies.
    Removes quotes from the song names.
    """
    # Group data by year and then by movie within each year
    grouped_data = {}
    for year, movie, song in data:
        if year not in grouped_data:
            grouped_data[year] = {}
        if movie not in grouped_data[year]:
            grouped_data[year][movie] = []
        grouped_data[year][movie].append(song)

    # Sort the years
    sorted_years = sorted(grouped_data.keys())

    # Start generating the Wikipedia table
    wikipedia_table = (
        "{| class=\"wikitable\"\n"
        "|- style=\"background:#ccc; text-align:center;\"\n"
        "! Year \n! Film !! Song\n"
    )

    for year in sorted_years:
        movies = grouped_data[year]
        num_movies = len(movies)
        year_rowspan = sum(len(songs) for songs in movies.values())

        first_movie = True
        for movie, songs in movies.items():
            num_songs = len(songs)
            movie_rowspan = num_songs

            for idx, song in enumerate(songs):
                wikipedia_table += "|-\n"
                if first_movie and idx == 0:
                    # Add Year with rowspan
                    wikipedia_table += f"| rowspan=\"{year_rowspan}\" | {year} \n"
                    # Add Movie with rowspan
                    wikipedia_table += f"| rowspan=\"{movie_rowspan}\" | ''{movie}'' \n"
                elif idx == 0:
                    # Add Movie with rowspan
                    wikipedia_table += f"| rowspan=\"{movie_rowspan}\" | ''{movie}'' \n"
                # Add Song without quotes
                wikipedia_table += f"| {song}\n"

            first_movie = False

    # Close the table
    wikipedia_table += "|}"

    return wikipedia_table

def main():
    all_data = []
    total_pages = 10  # Adjust this if there are more pages

    for page_num in range(1, total_pages + 1):
        print(f"Scraping page {page_num}...")
        page_data = scrape_page(page_num)
        all_data.extend(page_data)

    print("Generating Wikipedia table...")
    wikipedia_table = generate_wikipedia_table_with_rowspan(all_data)

    # Save the output to a text file
    output_path = "songs_wikipedia_table.txt"
    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(wikipedia_table)

    print(f"Wikipedia table has been saved to {output_path}")

if __name__ == "__main__":
    main()
