from flask import Flask, render_template, request
import requests
import sqlite3

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        artist_name = request.form['artist']
        sort = request.form["sort"]
        albums = search_albums(artist_name)
        save_albums_to_db(artist_name, albums)
        reverse = False
        if "reverse" in request.form and request.form["reverse"] == "True":
            reverse = True
        if "reverse" in request.form and request.form["reverse"] == "False":
            reverse = False
        return render_template('results.html', artist=artist_name, albums=albums, sort=sort, reverse=reverse)
    return render_template('index.html')


def search_albums(artist_name):
    API_KEY = '523532'
    URL = f'https://theaudiodb.com/api/v1/json/{API_KEY}/searchalbum.php?s={artist_name}'
    response = requests.get(URL)
    data = response.json()
    albums = data['album']
    return albums


def save_albums_to_db(artist_name, albums):
    conn = sqlite3.connect('albums.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS albums
                 (artist TEXT, album TEXT, year INTEGER)''')

    for album in albums:
        artist = artist_name
        album_name = album['strAlbum']
        year = album['intYearReleased']

        c.execute("INSERT INTO albums VALUES (?,?,?)", (artist, album_name, year))
        print(c.fetchone())

        if not c.fetchone():
            c.execute("INSERT INTO albums VALUES (?,?,?)", (artist, album_name, year))



    conn.commit()
    conn.close()


if __name__ == '__main__':
    app.run(debug=True)