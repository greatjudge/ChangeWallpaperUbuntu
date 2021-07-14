# ChangeWallpaperUbuntu
Change Wallpaper Ubuntu
Смена обоев рарбочего стола

1. changer.py
    Читает из файла  mainfile.json имя последнего файла и день смены. Если день отличаается, то происходит смена обой.
    changer.py можно поставить на автозапуск, установив необходимые зависимости.
    Полезные ссылки:
        https://pygobject.readthedocs.io/en/latest/getting_started.html - модуль python для работы с системой ubuntu.  
        https://itsecforu.ru/2020/04/05/%F0%9F%90%A7-%D0%BA%D0%B0%D0%BA-%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D1%82%D0%B8%D1%82%D1%8C-%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B-systemd-%D0%B1%D0%B5%D0%B7-%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2/ - про systemd
        
   
2. parser.py
    Парсит обои с сайта https://wallpaperscraft.ru/
   
   
   
Содержимое моего файла syncthing.service:  
    [Unit]
    Description=Смена обоев при смене дня

    [Service]
    Type=oneshot
    ExecStart=/home/greatjudge/WallPaper/ChangeWallpaperUbuntu/changer.py

    # Hardening
    SystemCallArchitectures=native
    MemoryDenyWriteExecute=true
    NoNewPrivileges=true

    [Install]
    WantedBy=default.target
