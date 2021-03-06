# AUTOGENERATED! DO NOT EDIT! File to edit: notebooks/01_datasets.loaders.ipynb (unless otherwise specified).

__all__ = ['create_multiclass_tag_manga_dataset', 'get_mangacover_dataloaders']

# Cell
import requests
from PIL import Image, UnidentifiedImageError
from pathlib import Path
from tqdm.auto import tqdm
from .internals.MangaDex import get_covers_for_all_tags

def create_multiclass_tag_manga_dataset(path, num_mangas=20):
    """Saves a dataset for the multiclassification problem of deriving the tags associated with
    a manga by its cover, in `path`.
    """
    print('Fetching manga metadata from the MangaDex API...')
    manga_df = get_covers_for_all_tags(num_mangas)
    folder = Path(f'{path}')
    folder.mkdir(parents=True, exist_ok=True)
    print(f'Saving data to {folder}...')
    for manga in tqdm(list(manga_df.itertuples())):
        my_file = folder/manga.filename
        if my_file.exists():
            manga_df.at[manga.Index, 'failed'] = False
            continue
        try:
            im = Image.open(requests.get(manga.url, stream=True).raw)
            im.save(folder/manga.filename)
            manga_df.at[manga.Index, 'failed'] = False
        except UnidentifiedImageError:
            print("Warning: Couldn't identify image file " + manga.filename + ". Skipping.")
            manga_df.at[manga.Index, 'failed'] = True
    metadata_csv_path = folder/'dataset.csv'
    print(f'Writing metadata csv file at {metadata_csv_path}')
    manga_df.to_csv(metadata_csv_path)
    print('Done.')

# Cell
from fastai.vision.all import *
import pandas as pd

def _get_mangacover_x(path, r): return path/r['filename']
def _get_mangacover_y(r): return r['tags'].split('|')

def get_mangacover_dataloaders(path):
    """Creates dataloaders based on the dataset in `path`"""
    folder = Path(f'{path}')
    mangas_df = pd.read_csv(folder/'dataset.csv')

    dblock = DataBlock(blocks=(ImageBlock, MultiCategoryBlock),
                       get_y=_get_mangacover_y, get_x=partial(_get_mangacover_x, folder),
                       item_tfms=Resize(128, ResizeMethod.Pad, pad_mode='zeros'))

    return dblock.dataloaders(mangas_df)