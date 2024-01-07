from fastapi import FastAPI, Path, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from starlette import status

from typing import Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Album:
    def __init__(self, id: int, title: str, artist: str, category: str,
                 year: int, rating: int):
        self.id = id
        self.title = title
        self.artist = artist
        self.category = category
        self.year = year
        self.rating = rating


class AlbumRequest(BaseModel):
    id: Optional[int] = Field(title='id is not needed')
    title: str = Field(min_length=1)
    artist: str = Field(min_length=1)
    category: str = Field(min_length=3, max_length=20)
    year: int = Field(gt=1950, lt=2030)
    rating: int = Field(gt=0, lt=6)


ALBUMS = [
    Album(1, 'Whos Next', 'The Who', 'rock', 1971, 5),
    Album(2, 'Led Zeppelin IV', 'Led Zeppelin', 'rock', 1971, 5),
    Album(3, 'Hunky Dory', 'David Bowie', 'rock', 1971, 5),
    Album(4, 'Electric Warrior', 'T. Rex', 'rock', 1971, 5),
    Album(5, 'Sticky Fingers', 'The Rolling Stones', 'rock', 1971, 5),
    Album(6, 'Master of Reality', 'Black Sabbath', 'metal', 1971, 5),    
]

@app.get("/albums", status_code=status.HTTP_200_OK)
async def get_all_albums():
    return ALBUMS

@app.get("/albums/{album_id}", status_code=status.HTTP_200_OK)
async def get_album_by_id(album_id:int=Path(gt=0)):
    for album in ALBUMS:
        if album.id==album_id:
            return album
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ALBUM_NOT_FOUND")

@app.get("/albums/rating/{rating}", status_code=status.HTTP_200_OK)
async def get_album_by_rating(rating:int=Path(gt=0, lt=6)):
    albums_list = []
    for album in ALBUMS:
        if album.rating==rating:
            albums_list.append(album.title)
    if len(albums_list)==0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ALBUM_NOT_FOUND")    
    return albums_list
    
@app.get("/albums/year/{year}", status_code=status.HTTP_200_OK)
async def get_album_by_year(year:int=Path(gt=1950, lt=2030)):
    albums_list = []
    for album in ALBUMS:
        if album.year==year:
            albums_list.append(album.title)
    if len(albums_list)==0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ALBUM_NOT_FOUND")    
    return albums_list

@app.post("/albums/create", status_code=status.HTTP_201_CREATED)
async def create_album(album_request:AlbumRequest):
    new_album = Album(**album_request.model_dump())
    ALBUMS.append(new_album)
    
@app.put("/albums/uptade", status_code=status.HTTP_204_NO_CONTENT)
async def update_album(album_request:AlbumRequest):
    album_changed=False
    for i in range(len(ALBUMS)):
        if ALBUMS[i].id==album_request.id:
            ALBUMS[i]=album_request
            album_changed=True
    if not album_changed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ALBUM_NOT_FOUND")   

@app.delete("/albums/delete_album/{album_id}", status_code=status.HTTP_200_OK)
async def delete_album(album_id:int=Path(gt=0)):
    album_changed=False
    for i in range(len(ALBUMS)):
        if ALBUMS[i].id == album_id:
            ALBUMS.pop(i)
            album_changed=True
            break
    if not album_changed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ALBUM_NOT_FOUND") 