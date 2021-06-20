# AUTOGENERATED! DO NOT EDIT! File to edit: notebooks/01_datasets.loaders.ipynb (unless otherwise specified).

__all__ = []

# Cell
import pandas as pd
from tqdm.auto import tqdm
from .internals.MangaDex import MangaDexClient


def _get_covers_for_all_tags(num_mangas=10):
    client = MangaDexClient("credentials.json")
    tags = client.get_manga_tags()
    mangas = [
        manga
        for _, tag_id in tqdm(tags.items())
        for manga in client.search_manga_tags_covers(total=20, includedTags=[tag_id])
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