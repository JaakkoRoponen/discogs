# ALBUM PRICES FROM DISCOGS.COM

This is an app for getting prices for albums from <https://discogs.com/>.

## Requirements

Please, provide an excel file with 'Cat', 'Artist' and 'Album' columns (you can use template.xlsx).

Cat stands for "catalog number". Multiple sheets are supported.

## Usage

### Windows

Copy and run discogs.exe from the dist folder.

(discogs.exe is the only file you'll need)

### Python

Install packages: `pip install -r requirements.txt`

Run app: `python discogs.py [-h] [-nu] [-nd] filename`

Optional arguments:

  -h, --help         show help message and exit

  -nu, --no-urls     don't search urls

  -nd, --no-details  don't search details

## Results

First searches the exact release based on the catalog number. If no results, then searches for the "master" by Artist and Album name.

In case of a match saves the album information, including album url and prices, to the source file.
