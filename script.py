import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.malayalasangeetham.info/songs.php?singers=P%20Jayachandran&singtype=solo&tag=Search&limit=470&page_num={}"

def scrape_page(page_num):
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
    Converts the extracted data into a Wikipedia table with rowspan for years,
    ensuring songs from the same year are grouped even if they appear across pages.
    """
    # Create a dictionary to group movies and songs by year
    grouped_data = {}
    for year, movie, song in data:
        if year not in grouped_data:
            grouped_data[year] = []
        grouped_data[year].append((movie, song))

    # Sort the years
    sorted_years = sorted(grouped_data.keys())

    # Start generating the Wikipedia table
    wikipedia_table = (
        "{| class=\"wikitable\"\n"
        "|- style=\"background:#ccc; text-align:center;\"\n"
        "! Year \n! Film !! Song\n"
    )

    # Loop through the grouped data and construct the table
    for year in sorted_years:
        songs = grouped_data[year]
        rowspan = len(songs)  # Number of rows for this year
        wikipedia_table += f"|-\n| rowspan=\"{rowspan}\" | {year}\n"

        # Add the first movie and song
        first_movie, first_song = songs[0]
        wikipedia_table += f"! ''{first_movie}''\n| \"{first_song}\"\n"

        # Add the remaining movies and songs
        for movie, song in songs[1:]:
            wikipedia_table += "|-\n"
            wikipedia_table += f"! ''{movie}''\n| \"{song}\"\n"

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

    output_path = "songs_wikipedia_table.txt"
    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(wikipedia_table)

    print(f"Wikipedia table has been saved to {output_path}")

if __name__ == "__main__":
    main()
