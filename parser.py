# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os.path

from bs4 import BeautifulSoup
import requests
from time import sleep
from abc import ABC, abstractmethod

class SaveWallpaper:
    def __init__(self, domein, basedir):
        self.domein = domein
        self.basedir = basedir

    def save_wallpapers(self, url, namedir, npages=1):
        domein = self.domein
        url = url + 'page{}'
        print('url', url)
        for i in range(1, npages+1):
            urls = tuple(map(lambda x: domein + x, self._get_image_urls(domein + url.format(i))))
            for image_url in urls:
                downloaded_url = self._get_down_page(image_url)
                if downloaded_url is None: continue
                self._save_image(self._get_down_url(domein + downloaded_url), os.path.join(self.basedir, namedir))

    @staticmethod
    def _get_html(url):
        sleep(5)
        res = requests.get(url)
        if not res.ok:
            print(res.text)
            print('res no ok')
            print('url', url)
        return res.text

    @staticmethod
    def _get_content(url):
        res = requests.get(url)
        return res.content

    @staticmethod
    def _get_filename(url):
        print('name:', url.split('/')[-1])
        return url.split('/')[-1]

    def _get_image_urls(self, page_url):
        soup = BeautifulSoup(self._get_html(page_url), 'lxml')
        images = soup.find_all('li', class_='wallpapers__item')
        urls = list()
        for image in images:
            url = image.find('a', class_='wallpapers__link').get('href')
            urls.append(url)
        return urls

    def _get_down_page(self, image_url):
        soup = BeautifulSoup(self._get_html(image_url), 'lxml')
        image_div = soup.find_all('section')[1].find_all('div', class_='resolutions__table')[-2]
        a = image_div.find('a', class_='resolutions__link')
        if a.text == '1920x1080':
            return a.get('href')
        else:
            print(image_url, 'Something wrong')
            return None

    def _get_down_url(self, url):
        soup = BeautifulSoup(self._get_html(url), 'lxml')
        return soup.find('a', class_='gui-button gui-button_full-height').get('href')

    def _save_image(self, url, dir):
        with open(os.path.join(dir, self._get_filename(url)), 'wb') as file:
            file.write(self._get_content(url))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    wp = WallPaperGetter('https://wallpaperscraft.ru/', '/home/greatjudge/wallpapers/')
    wp.save_wallpaper('catalog/city/', 'city', 3)
    wp.save_wallpaper('catalog/space/', 'space', 3)