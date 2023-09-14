from bs4 import BeautifulSoup
import time
import re
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
        city="Paris",
        notif_url=None,
        verbose=False,
        ):
    "simple loop that checks if tickets are available for each movie"

    avail = []
    noavail = []
    errors = []

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

        # look for tickets
        tickets_url = f"https://www.allocine.fr/seance/film-{film_id}"

        # load the ticket page
        page = requests.get(tickets_url)
        soup = BeautifulSoup(page.content, "html.parser")

        # check if contains the city name greyed out or not
        if not soup.find("a", {"title": city, "class": "disabled"}):
            pr(f"Tickets available in {city} for '{name}'\n")
            avail.append(name)
        else:
            pr(f"No tickets available for {name}\n")
            if not soup.find("span", {"title": city, "class": "disabled"}):
                pr(f"Probable error when loading ticket page for {name}")
                errors.append(name)
            noavail.append(name)

        # reduce load to avoid bot detection
        time.sleep(0.1)

    pr("\nSummary:")
    pr("NOT available:\n *  " + '\n *  '.join(noavail) + "\n")
    pr("Available:\n *  " + '\n *  '.join(avail) + "\n")
    pr("Errors:\n *  " + "\n*  ".join(errors) + "\n")

    if notif_url is not None:
        notifier(
                message=output,
                notif_url=notif_url
                )


if __name__ == "__main__":
    fire.Fire(main)
