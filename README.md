# ALBUM PRICES FROM DISCOGS.COM

This is an app for getting prices for albums from <https://www.discogs.com/>

## Requirements

Please, provide an excel file with 'Cat', 'Artist' and 'Album' columns.

Cat stands for "catalog number". Multiple sheets are supported.

## Usage

windows: (you'll only need the discogs.exe from the dist folder)

`discogs [-h] [-nu] [-nd] filename`

source:

`python discogs.py [-h] [-nu] [-nd] filename`

optional arguments:

  -h, --help         show help message and exit

  -nu, --no-urls     don't search urls

  -nd, --no-details  don't search details

## Results

First searches the exact release based on the catalog number. If no results, then searches for the "master" by Artist and Album name.

In case of a match saves the album information, including album url and prices, to the source file.
