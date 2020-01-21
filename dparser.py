"""
Discogs.com parser
"""

import requests

from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz


class Parser():
    """Parser for Discogs.com queries"""

    def __init__(self):
        self.url = 'https://www.discogs.com'

    def search_album(self, query, query_by_cat=True):
        """Search for an album in Discoqs"""
        query_type = 'release' if query_by_cat else 'master'
        params = {'type': query_type, 'q': query}
        try:
            website = requests.get(f'{self.url}/search/', params=params)
        except requests.exceptions.RequestException:
            return None
        return website.text

    def find_matching_search_result(self, website, match=''):
        """Return first 80 percent accurate matches url"""
        try:
            soup = BeautifulSoup(website, 'html.parser')
        except TypeError:  # no website
            return None
        anchors = soup.find_all('a', class_='search_result_title')
        for a in anchors:
            if fuzz.partial_ratio(a['title'].lower(), match.lower()) > 80:
                return a['href']
        return None

    def get_album(self, album_url):
        """Return album's website"""
        try:
            website = requests.get(album_url)
        except requests.exceptions.RequestException:
            return None
        return website.text

    def find_album_details(self, website):
        """Find album's details on the album website"""
        try:
            soup = BeautifulSoup(website, 'html.parser')
        except TypeError:  # no website
            return None
        details = {}

        profile = soup.find(class_='profile')
        for detail in [
            'Label',
            'Format',
            'Country',
            'Released',
            'Genre',
        ]:
            try:
                details[detail] = ''.join(list(
                    profile.find('div', string=f'{detail}:')
                    .next_sibling.next_sibling.stripped_strings))
            except AttributeError:
                continue

        statistics = soup.find(id='statistics')
        for detail in ['Have', 'Want', 'Last Sold']:
            try:
                details[detail] = \
                    statistics.find('h4', string=f'{detail}:') \
                    .next_sibling.next_sibling.string
            except AttributeError:
                continue

        for detail in ['Lowest', 'Median', 'Highest']:
            try:
                details[detail] = \
                    str(statistics.find(string=f'{detail}:')
                        .parent.next_sibling.string).strip()
            except AttributeError:
                continue

        marketplace = soup.find(class_='marketplace_for_sale_count')
        try:
            count = marketplace.find('strong').string
            from_price = marketplace.find(class_='price').string
            details['Market'] = f'{count} from {from_price}'
        except AttributeError:
            pass

        return details
