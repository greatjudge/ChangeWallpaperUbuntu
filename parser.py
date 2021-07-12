import requests

from bs4 import BeautifulSoup
from time import sleep

from itertools import repeat
from functools import reduce

from pathlib import Path

from typing import Iterable, Optional, Union, Sequence

from abc import ABC, abstractmethod


class Requester:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {'User-Agent': ''}

    def get_html(self, url, tsleep=5):
        sleep(tsleep)
        res = self.session.get(url)
        if not res.ok:
            print('res no ok')
            print('url', url)
            print(res.text)
            return None
        return res.text

    def get_content(self, url):
        res = self.session.get(url)
        return res.content

    def get_html_list(self, urls):
        for url in urls:
            html = self.get_html(url)
            if html is not None:
                yield html


class AbcPSWallpaper(ABC):
    domein = 'https://wallpaperscraft.ru/'

    def __init__(self, basedir: str, resolution='1920x1080'):
        self.basedir = Path(basedir)
        self.resolution = resolution
        self.requester = Requester()

    @abstractmethod
    def save_wallpapers(self, url: str, namedir: str, npages: int = 1):
        """
                Parse pages and save images from s  ite self.domain / namedir
                url: 'catalog/name_catalog/' must conteins '/' in the end.
        """
        pass

    @staticmethod
    def _get_image_urls(html: str) -> Iterable[str]:
        """Parse html to find image urls"""
        soup = BeautifulSoup(html, 'lxml')
        images = soup.find_all('li', class_='wallpapers__item')
        urls = list()
        for image in images:
            url = image.find('a', class_='wallpapers__link').get('href')
            urls.append(url)
        return urls

    def _get_down_page_url(self, html: str) -> Optional[str]:
        """Parse image page for find download page url"""
        soup = BeautifulSoup(html, 'lxml')
        image_div = soup.find_all('section')[1].find_all('div', class_='resolutions__table')[-2]
        a = image_div.find('a', class_='resolutions__link')
        if a.text == self.resolution:
            return a.get('href')
        else:
            return None

    @staticmethod
    def _get_down_url(html: str) -> str:
        """Parse download page url for find download url"""
        soup = BeautifulSoup(html, 'lxml')
        return soup.find('a', class_='gui-button gui-button_full-height').get('href')

    @staticmethod
    def _get_filename(url: str) -> str:
        print('name:', url.split('/')[-1])
        return url.split('/')[-1]

    def _save_image(self, url: str, dir: Path):
        if not dir.exists():
            dir.mkdir()
        path = dir / self._get_filename(url)
        if not path.exists():
            with path.open('wb') as file:
                file.write(self.requester.get_content(url))
            print()
            print('save:', path)


class PSWallpaper(AbcPSWallpaper):
    def save_wallpapers(self, url: str, namedir: Union[str, Path], npages=1):
        url = url + 'page{}'
        page_urls = (url.format(i) for i in range(1, npages+1))
        download_urls = reduce(lambda x,y: x+y, map(self.parse_page, page_urls))
        print('Download urls:', len(download_urls)); print(download_urls)
        self._save_images(download_urls, self.basedir / namedir)

    def parse_page(self, page_url: str) -> Sequence:
        urls = map(lambda x: self.domein + x, self._get_image_urls(self.requester.get_html(self.domein + page_url)))
        download_page_urls = map(lambda x: self.domein + x,
                                 filter(lambda x: x is not None,
                                        map(self._get_down_page_url, self.requester.get_html_list(urls))))
        download_urls = filter(lambda x: x is not None,
                               map(self._get_down_url, self.requester.get_html_list(download_page_urls)))
        return list(download_urls)

    def _save_images(self, img_urls: Iterable[str], dir: Path):
        list(map(self._save_image, img_urls, repeat(dir)))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    wp = PSWallpaper('/home/greatjudge/Wallpapers/')
    # wp.save_wallpapers('catalog/city/', 'city', 3)
    # wp.save_wallpapers('catalog/space/', 'space', 3)
    wp.save_wallpapers('catalog/vector/', 'vector', 3)
