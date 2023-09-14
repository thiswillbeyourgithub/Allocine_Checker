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
        notif_url=None,
        verbose=False,
        ):
    "simple loop that checks if tickets are available for each movie"

    avail = []
    noavail = []
    output = ""
    if verbose:
        pr = print
    else:
        def pr(line):
            nonlocal output
            output += "\n" + line
            print(line)

    for name, url in urls.items():
        pr(f"Name: '{name}'")

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
        #pr(f"Title: {article.title}")
        text = article.cleaned_text
        #raw = article.raw_html

        # either the page loaded silently again to the initial page
        if orig_text.strip() == text.strip():
            pr(f"No tickets available for {name}\n")
            noavail.append(name)

        # or the page is displaying the tickets
        else:
            pr(f"Tickets available in Paris for {name}\n")
            avail.append(name)

        # reduce load to avoid bot detection
        time.sleep(1)

    pr(f"\nRecap:")
    pr("NOT available: " + ', '.join(noavail) + "\n")
    pr("Available: " + ', '.join(avail) + "\n")


    if notif_url is not None:
        notifier(
                message=output,
                notif_url=notif_url
                )

if __name__ == "__main__":
    fire.Fire(main)
