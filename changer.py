#! /usr/bin/python3
import json
import os

from gi.repository import Gio
from pathlib import Path
from itertools import cycle

from datetime import date
from dateutil.parser import parse

from dotenv import load_dotenv

class ChWallpaper:
    def __init__(self, dotenv_path: str):
        load_dotenv(dotenv_path)
        directory_str = os.getenv('WALLPAPERS_DIR_PATH')
        self.mainfile = Path(os.getenv('MAINFILE_PATH'))
        self.directory = Path(directory_str)
        self.Directories = cycle(self.directory.iterdir())

    def change(self):
        data = self.read_data()
        last_date = parse(data['date']).date()
        if last_date != date.today():
            filename = self._get_new_filename(data)
            self.chwall(str(filename))
            self.write_ld(str(filename), date.today().isoformat())

    def _get_new_filename(self, data: dict) -> Path:
        last_file = Path(data['last'])
        last_dir = last_file.parent
        files_in_dir = list(last_dir.iterdir())
        index_last = files_in_dir.index(last_file)
        if index_last == len(files_in_dir) - 1:
            current_dir = last_dir
            for dir in self.Directories:
                if dir == current_dir:
                    break
            current_dir = next(self.Directories)
            filename = list(current_dir.iterdir())[0]
        else:
            filename = files_in_dir[index_last + 1]
        return filename

    @staticmethod
    def chwall(filename: str):
        gsettings = Gio.Settings.new('org.gnome.desktop.background')
        gsettings.set_string('picture-uri', filename)

    def read_data(self) -> dict:
        if not self.mainfile.exists():
            with self.mainfile.open('w') as file:
                json.dump({'date': date.today().isoformat(),
                           'last': str(self._first_filename())},
                          file)
        with self.mainfile.open() as file:
           data = json.load(file)
        return data

    def write_ld(self, last: str, date: str):
        data = dict()
        data['date'] = date
        data['last'] = last
        self.write_data(data)

    def write_data(self, data: dict):
        with self.mainfile.open('w') as file:
            json.dump(data, file)

    def _first_filename(self) -> Path:
        return next(next(self.directory.iterdir()).iterdir())


def main():
    chw = ChWallpaper('/home/greatjudge/WallPaper/ChangeWallpaperUbuntu/.env')
    chw.change()


if __name__ == '__main__':
    main()




