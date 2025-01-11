<p align="center">
<img src="Logo.png"/>
</p>

_______
# Sangeetha Pattika

Sangeetha Pattika is a project that scrapes song data from [Malayalasangeetham.info](https://www.malayalasangeetham.info/), processes it, and generates a Wikipedia-compatible table with links to relevant Malayalam Wikipedia articles.

---

## Features

1. **Data Scraping**:
   - Extracts song names, movie titles, and release years from Malayalasangeetham.info across multiple pages.
2. **Wikipedia Table Generation**:
   - Formats the data into a table that can be directly used in Wikipedia articles.
3. **Article Linking**:
   - Automatically searches for and links to the most relevant Wikipedia article for each movie.
   - Prioritizes articles ending with `_(ചലച്ചിത്രം)` for accuracy.
   - Falls back to similarity-based matching (>75%) if no exact match exists.
4. **Error Handling**:
   - Handles cases where no relevant Wikipedia article is found by italicizing the movie name.

---

## Usage

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. Create a virtul env and Install the required Python dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
### 2. Run the Script

```bash
python scraper.py
```

### 3. Output

The script generates a file named `songs_wikipedia_table.txt` in the project directory. This file contains the Wikipedia-compatible table.

---

## How It Works

### Scraper Logic

1. **Fetch Pages**:
   - Iterates through all pages of Malayalasangeetham.info to extract song data.
2. **Data Parsing**:
   - Extracts song name, movie title, and release year from each page.
3. **Wikipedia Search**:
   - For each movie, searches the Malayalam Wikipedia API for a matching article.
   - Prioritizes articles ending with `(ചലച്ചിത്രം)`.
   - Falls back to exact or similarity-based matches if no suffix article is found.
4. **Output**:
   - Formats the scraped data into a Wikipedia-compatible table and saves it to a `.txt` file.

---


## Troubleshooting

### Common Issues

1. **No Output**:
   - Ensure the Malayalasangeetham.info website is accessible.
   - Check your internet connection.

2. **Missing Wikipedia Links**:
   - Movies without relevant Wikipedia articles are italicized in the table.
   - Verify the movie name's spelling on Wikipedia.

---

## Contributions

Feel free to submit issues, suggestions, or pull requests. This is an open project, and contributions are welcome!

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.
