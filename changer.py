import json

from gi.repository import Gio
from pathlib import Path
from itertools import cycle

from datetime import date
from dateutil.parser import parse


class ChWallpaper:
    directory_str = '/home/greatjudge/Wallpapers/'
    mainfile = Path('mainfile.json')
    directory = Path(directory_str)
    Directories = cycle(directory.iterdir())

    def change(self):
        data = self.read_data()
        last_date = parse(data['date']).date()
        if last_date != date.today(): # It need to refactoring
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
            self.chwall(filename)
            self.write_ld(str(filename), date.today().isoformat())

    def chwall(self, filename):
        print('filename', filename)
        gsettings = Gio.Settings.new('org.gnome.desktop.background')
        gsettings.set_string('picture-uri', str(filename))

    def read_data(self) -> dict:
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


def main():
    chw = ChWallpaper()
    chw.change()


if __name__ == '__main__':
    main()




