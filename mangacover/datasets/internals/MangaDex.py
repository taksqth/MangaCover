# AUTOGENERATED! DO NOT EDIT! File to edit: notebooks/00_datasets.internals.mangadex.ipynb (unless otherwise specified).

__all__ = ['MangaDexClient', 'get_covers_for_all_tags']

# Cell
import requests
import json


class MangaDexClient:
    """Client for the MangaDex API"""

    def __init__(self, credentials_file):
        with open(credentials_file) as config_file:
            data = config_file.read()

        response = requests.post(
            "https://api.mangadex.org/auth/login", json=json.loads(data)
        )
        content = json.loads(response.content)
        self.refresh_token = content["token"]["refresh"]
        self.session_token = content["token"]["session"]

    def get_manga_tags(self):
        """Returns a dict from human readable tag names to tag_ids for each tag in the mangadex database"""
        response = requests.get(
            "https://api.mangadex.org/manga/tag",
            headers={
                "Authorization": f"Bearer {self.session_token}",
            },
        )
        content = json.loads(response.content)
        return {
            item["data"]["attributes"]["name"]["en"]: item["data"]["id"]
            for item in content
        }

    def search_manga_tags_covers(
        self, total=None, limit=100, offset=0, includedTags=None, excludedTags=None
    ):
        """Gets a list of manga with id, tags and cover image filenames"""
        contents = []
        while total is None or offset < total:
            response = requests.get(
                "https://api.mangadex.org/manga",
                params={
                    "limit": limit if not total else min(limit, total - offset),
                    "offset": offset,
                    "includedTags[]": includedTags,
                    "excludedTags[]": excludedTags,
                    "includes[]": "cover_art",
                },
                headers={
                    "Authorization": f"Bearer {self.session_token}",
                },
            )
            content = json.loads(response.content)
            if not total:
                total = content["total"]
            contents.append(content)
            offset += limit

        return [
            {
                "mangaId": result["data"]["id"],
                "tags": [
                    tag["attributes"]["name"]["en"]
                    for tag in result["data"]["attributes"]["tags"]
                ],
                "cover_art_filenames": [
                    relationship["attributes"]["fileName"]
                    for relationship in result["relationships"]
                    if relationship["type"] == "cover_art"
                ],
            }
            for content in contents
            for result in content["results"]
        ]

# Cell
import pandas as pd
from tqdm.auto import tqdm

def get_covers_for_all_tags(num_mangas=20):
    """Returns a pandas DataFrame with covers image urls for each tag in the MangaDex database.

    It may be possible for a manga to show up in the query for multiple different tags, so we
    deduplicate those cases.

    TODO: There seems to be an issue with the API where only one cover image is returned for each
    manga. We need to investigate this further, so we do not run into the issue of having too much
    data to handle unexpectedly if this behavior changes suddenly.
    """
    try:
        client = MangaDexClient('credentials.json')
    except FileNotFoundError as e:
        e.strerror = "The current version expects a credentials.json file at cwd."
        raise e
    tags = client.get_manga_tags()
    mangas = [
        manga
        for _, tag_id in tqdm(tags.items())
        for manga in client.search_manga_tags_covers(total=num_mangas, includedTags=[tag_id])
    ]

    # Deduplicate mangas in list by mangaId
    seen = set()
    mangas = [
        seen.add(manga["mangaId"]) or manga
        for manga in mangas
        if manga["mangaId"] not in seen
    ]

    return pd.DataFrame(
        [
            {
                "mangaId": manga["mangaId"],
                "url": f'https://uploads.mangadex.org/covers/{manga["mangaId"]}/{filename}',
                "filename": f'{manga["mangaId"]}_{filename}',
                "tags": "|".join(manga["tags"]),
            }
            for manga in mangas
            for filename in manga["cover_art_filenames"]
        ]
    )