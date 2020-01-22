"""
A Project to get prices for Albums from discogs.com
"""

from argparse import ArgumentParser
import sys

import pandas as pd

from dparser import Parser
from utils.pexel import Pexel


def find_urls(data, parser):
    """Search and add album url to album data"""
    for index, album in data.df.iterrows():
        # Only search for url when it doesn't exist
        if 'Url' in album and album.Url:
            continue

        print('Searching url for %s' %
              album[['Cat', 'Artist', 'Album']].to_dict())

        # First search by catalog number and then by artist and album
        queries = [album.Cat, f'{album.Artist} {album.Album}']
        for query_index, query in enumerate(queries):
            if not query:  # no album cat. number
                continue
            query_by_cat = True if query_index == 0 else False
            website = parser.search_album(query, query_by_cat=query_by_cat)
            first_search_result = parser.find_matching_search_result(
                website, match=album.Album)
            if first_search_result:
                print(f'..Found {first_search_result}\n')
                data.add_data_to_row(index, {
                    'Match by cat': 'Yes' if query_by_cat else 'No',
                    'Url': f'{parser.url}{first_search_result}'})
                break
        else:
            print('..Not found\n')


def find_details(data, parser):
    """Search and add album details to album data"""
    for index, album in data.df.iterrows():
        if 'Url' not in album:
            break

        print('Searching details for %s' %
              album[['Cat', 'Artist', 'Album']].to_dict())

        album_website = parser.get_album(album.Url)
        details = parser.find_album_details(album_website)
        if details:
            print(f'..Found {details}\n')
            data.add_data_to_row(index, details)
        else:
            print('..Not found\n')


def main(args):
    data = Pexel(args.filename)
    data.df.fillna('', inplace=True)

    # Check that all required columns exist in the source file
    if not all(col in data.df.columns for col in ['Cat', 'Artist', 'Album']):
        sys.exit("Error: File must have columns 'Cat', 'Artist' and 'Album'")

    parser = Parser()

    if not args.no_urls:
        find_urls(data, parser)
    if not args.no_details:
        find_details(data, parser)

    data.save()
    print('Done!')


if __name__ == '__main__':

    # define command line args
    args_parser = ArgumentParser()
    args_parser.add_argument('filename', help='filename')
    args_parser.add_argument('-nu', '--no-urls', action='store_true',
                             help="don't search urls")
    args_parser.add_argument('-nd', '--no-details', action='store_true',
                             help="don't search details")

    # get command line args
    args = args_parser.parse_args()

    main(args)
