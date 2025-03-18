from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

BASE_URL = "https://music-fa.com/search/"


def get_data(query):
    url = BASE_URL + query.replace(" ", "%20")
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return {"error": True, "message": "Failed to fetch data"}
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    results = []
    songs = soup.select("article.mf_pst")
    
    for song in songs:
        title = song.get("data-artist", "Unknown Artist")
        song_id = song.get("data-id", "N/A")
        download_link = song.select_one("span.play")
        image = song.select_one("img.wp-post-image")
        
        results.append({
            "id": song_id,
            "title": title,
            "download_link": download_link["data-song"] if download_link else "N/A",
            "image": image["src"] if image else "N/A"
        })
    
    return results if results else {"message": "Oops! No results found."}


@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": True, "message": "Query parameter is required."}), 400
    
    result = get_data(query)
    return jsonify({"dev": "@dnl_loop", "channel": "@psychoxyz", "data": result})


if __name__ == "__main__":
    app.run(debug=True)
