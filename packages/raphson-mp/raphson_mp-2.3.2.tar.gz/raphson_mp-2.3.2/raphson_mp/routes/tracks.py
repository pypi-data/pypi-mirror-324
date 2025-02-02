import dataclasses
import logging
from sqlite3 import Connection

from aiohttp import web

from raphson_mp import scanner, search
from raphson_mp.auth import User
from raphson_mp.decorators import route
from raphson_mp.music import Track

log = logging.getLogger(__name__)


@route("/filter")
async def route_filter(request: web.Request, conn: Connection, _user: User):
    last_modified = scanner.last_change(conn, request.query["playlist"] if "playlist" in request.query else None)

    if request.if_modified_since and last_modified <= request.if_modified_since:
        raise web.HTTPNotModified()

    query = "SELECT path FROM track WHERE true"
    params: list[str | int] = []
    if "playlist" in request.query:
        query += " AND playlist = ?"
        params.append(request.query["playlist"])

    if "artist" in request.query:
        query += " AND EXISTS(SELECT artist FROM track_artist WHERE track = path AND artist = ?)"
        params.append(request.query["artist"])

    if "album_artist" in request.query:
        query += " AND album_artist = ?"
        params.append(request.query["album_artist"])

    if "album" in request.query:
        query += " AND album = ?"
        params.append(request.query["album"])

    if "year" in request.query:
        query += " AND year = ?"
        params.append(int(request.query["year"]))

    if "has_metadata" in request.query and request.query["has_metadata"] == "1":
        # Has at least metadata for: title, album, album artist, artists
        query += """AND title NOT NULL
                    AND album NOT NULL
                    AND album_artist NOT NULL
                    AND EXISTS(SELECT artist FROM track_artist WHERE track = path)"""

    if "tag" in request.query:
        query += " AND EXISTS(SELECT tag FROM track_tag WHERE track = path AND tag = ?)"
        params.append(request.query["tag"])

    if "order" in request.query:
        order = request.query["order"]
        if order == "title":
            query += " ORDER BY title"
        elif order == "ctime":
            query += " ORDER BY ctime"
        else:
            log.warning("ignoring invalid order: %s", order)

    limit = int(request.query.get("limit", 5000))
    query += f" LIMIT {limit}"

    offset = int(request.query.get("offset", 0))
    query += f" OFFSET {offset}"

    result = conn.execute(query, params)
    tracks = [Track.by_relpath(conn, row[0]) for row in result]

    response = web.json_response({"tracks": [track.info_dict() for track in tracks]})
    response.last_modified = last_modified
    response.headers["Cache-Control"] = "no-cache"  # always verify last-modified
    return response


@route("/search")
async def route_search(request: web.Request, conn: Connection, _user: User):
    query = request.query["query"]
    tracks = search.search_tracks(conn, query)
    albums = [dataclasses.asdict(album) for album in search.search_albums(conn, query)]
    return web.json_response({"tracks": [track.info_dict() for track in tracks], "albums": albums})


@route("/tags")
async def route_tags(_request: web.Request, conn: Connection, _user: User):
    result = conn.execute("SELECT DISTINCT tag FROM track_tag ORDER BY tag")
    tags = [row[0] for row in result]
    return web.json_response(tags)
