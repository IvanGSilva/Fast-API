from fastapi import FastAPI, Body

app = FastAPI()

ALBUMS = [
    {'title': 'Whos Next', 'artist': 'The Who', 'category': 'rock'},
    {'title': 'Led Zeppelin IV', 'artist': 'Led Zeppelin', 'category': 'rock'},
    {'title': 'Hunky Dory', 'artist': 'David Bowie', 'category': 'rock'},
    {'title': 'Electric Warrior', 'artist': 'T. Rex', 'category': 'rock'},
    {'title': 'Sticky Fingers', 'artist': 'The Rolling Stones', 'category': 'rock'},
    {'title': 'Master of Reality', 'artist': 'Black Sabbath', 'category': 'metal'},
]

@app.get("/albums")
async def read_all_albums():
    return ALBUMS

@app.get("/albums/{album_title}")
async def read_album(album_title: str):
    for album in ALBUMS:
        if album.get('title').casefold() == album_title.casefold():
            return album
        
@app.get("/albums/category/{category}")
async def read_album(category: str):
    albums_to_return = []
    for album in ALBUMS:
        if album.get('category').casefold() == category.casefold():
            albums_to_return.append(album)
    return albums_to_return
        
@app.get("/albums/artist/{artist}")
async def read_album(artist: str):
    albums_to_return = []
    for album in ALBUMS:
        if album.get('artist').casefold() == artist.casefold():
            albums_to_return.append(album)
    return albums_to_return

@app.post("/albums/create_album")
async def create_album(new_album=Body()):
   ALBUMS.append(new_album)


@app.put("/albums/update_album")
async def update_album(updated_album=Body()):
    for i in range(len(ALBUMS)):
        if (ALBUMS[i].get('title').casefold() ==
                updated_album.get('title').casefold()):
            ALBUMS[i] = updated_album

@app.delete("/albums/delete_album/{album_title}")
async def delete_album(album_title: str):
    for i in range(len(ALBUMS)):
        if ALBUMS[i].get('title').casefold() == album_title.casefold():
            ALBUMS.pop(i)
            break
        