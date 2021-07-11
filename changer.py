from gi.repository import Gio
import os

directory = '/home/greatjudge/Wallpapers/city'


class ChWallpaper:
    def __init_(self, directory):
        self.directory = directory

    def chwall(filename, directory=None):
        dirname = self.directory if directory is None else directory
        gsettings = Gio.Settings.new('org.gnome.desktop.background')
        gsettings.set_string('picture-uri', os.path.join(self.directory, filename))