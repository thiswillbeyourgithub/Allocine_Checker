import time
import re
from goose3 import Goose
import requests
import fire

from urls import urls

def notifier(message, notif_url):
    "send a notification to my phone using ntfy"
    return requests.post(
        url=notif_url,
        headers={"Title": "Movie tickets"},
        data=message.encode("utf-8"),
        )



def main(
        send_notification=True,
        notif_url=None,
        ):
    "simple loop that checks if tickets are available for each movie"

    for name, url in urls.items():
        print(f"Name: '{name}'")

        # get the film id
        film_id = re.findall("https://www.allocine.fr/film/fichefilm_gen_cfilm=(\d+).html", url)
        assert len(film_id) == 1, f"Invalid length: '{film_id}'"
        film_id = int(film_id[0])
        assert isinstance(film_id, int), f"invalid type: {film_id}"

        # look for tickets close to Paris
        tickets_url = f"https://www.allocine.fr/seance/film-{film_id}/pres-de-115755/"

        # load the original page
        g = Goose()
        orig_article = g.extract(url)
        orig_text = orig_article.cleaned_text
        #orig_raw = orig_article.raw_html

        # load the ticket page
        g = Goose()
        article = g.extract(tickets_url)
        print(f"Title: {article.title}")
        text = article.cleaned_text
        #raw = article.raw_html

        # either the page loaded silently again to the initial page
        if orig_text.strip() == text.strip():
            print(f"No tickets available for {name}")

        # or the page is displaying the tickets
        else:
            print(f"Tickets available for {name}")
            if send_notification:
                assert notif_url is not None, "you have to supply a notif_url if you set send_notification to True"
                notifier(
                        message=f"Tickets available for {name}",
                        notif_url=notif_url
                        )

        # reduce load to avoid bot detection
        time.sleep(1)

if __name__ == "__main__":
    fire.Fire(main)
