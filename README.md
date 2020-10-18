# roks
Адаптація [wumb-to-sqlite](https://github.com/eyeseast/wumb-to-sqlite) для [Радіо Рокс](https://www.radioroks.ua/). 

Завантажує [плейлист](https://www.radioroks.ua/playlist/) за період. 


## Installation
Віртуальне середовище: 
```
$ python -m venv env
$ env/Scripts/activate
$ python -m pip install -r requirements.txt 
```

## Usage
```
$ python roks/cli.py playlist --help
Usage: cli.py playlist [OPTIONS] DATABASE

  Download daily playlists, for a date or a range

Options:
  -t, --table TEXT
  --date [%d-%m-%Y]
  --since [%d-%m-%Y]
  --until [%d-%m-%Y]
  --delay INTEGER     [default: 1]
  --help              Show this message and exit.
```
Плейлист за сьогодні:
```
python roks/cli.py playlist roks.db
```
Плейлист за період:
```
python roks/cli.py playlist roks.db --since 12-10-2020 --until 18-10-2020
```

Топ виконавців з SQLite:
```SQL
SELECT artists.value, COUNT(*) AS num
FROM playlist
LEFT JOIN artists ON playlist.artist = artists.id
GROUP BY artist
ORDER BY num DESC;
```