# Allocine Checker
Very simple python program to check if a movie is currently in theaters around you. Especially useful for old movies.

## Usage
* download `allocine_checker.py`
* create a file `urls.py` that contains a python dictionary like so:
```
urls = {
 "Stalker": "https://www.allocine.fr/film/fichefilm_gen_cfilm=702.html",
 }
```
* launch the script with `python allocine_checker.py`

## Note
* If you want to receive a notification on your phone, setup [the great ntfy.sh](https://ntfy.sh/) then supply the url like so : `python allocine_checker.py --notif_url=YOUR_NTFY_URL`
* You can use cron to setup a weekly check like me.
