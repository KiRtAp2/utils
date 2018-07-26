#!/usr/bin/env python3

from html.parser import HTMLParser
from urllib.parse import urlparse
from sys import argv, stderr
import requests
import re


# Parts of the original URL
netloc = None
scheme = None
scheme_netloc_sep = None

# The search query
query = None

seen_sites = set()


class Parser(HTMLParser):
    
    def handle_starttag(self, tag, attrs):
        # When we get an <a> tag, we will go deeper into the search tree - if it's linking to the same site
        if tag == "a":
            for att in attrs:
                
                # We're only interested in links, not classes or other attributes
                if att[0] != "href":
                    continue

                # Internal links on a webpage should be relative
                # Here, we get rid of any absolute links (hopefully)
                if re.match(r"^http(s)?://", att[1]):
                    continue

                # We don't really want to mail people in this app
                if att[1].startswith("mailto:"):
                    continue

                # we do not want to look at pdfs, pictures etc.
                if re.match(r".+\.[a-zA-Z]{2,4}$", att[1]):

                    # we do, however, want to look at html pages
                    if not (att[1].endswith(".html") or att[1].endswith(".htm")): 
                        continue

                # We don't want to follow id links
                if "#" in att[1]:
                    idx = att[1].find("#")
                    att = att[0], att[1][:idx]

                # Some addresses have a preceding and succeding \' for some reason
                if att[1].startswith("\\'") and att[1].endswith("\\'"):
                    s = att[1][2:-2]
                    att = att[0], s
                
                # sometimes, these strippings cause us to end up with an empty string
                if len(att[1]) < 1:
                    continue

                if att[1][0] == "/":
                    new_site = scheme + scheme_netloc_sep + netloc + att[1]
                else:
                    new_site = scheme + scheme_netloc_sep + netloc + "/" + att[1]

                scan_site(new_site)

    def handle_data(self, data):
        if query in data.lower():
            print("Found on {}".format(curr_site))


def scan_site(url):
    global curr_site
    if url in seen_sites:
        return

    seen_sites.add(url)

    pars = Parser()
    req = requests.get(url)
    try:
        html = req.content.decode("UTF-8")
    except UnicodeDecodeError:
        # If the website gives us pictures that don't end in an extension
        return
    pars.feed(req.content.decode("UTF-8"))


def main():
    global query, netloc, scheme, scheme_netloc_sep

    if len(argv) < 3:
        print("Usage: {} <url> query with optional spaces".format(argv[0]))
        print("Please provide a website to scan and a string to search for.")
        quit()

    if not re.match(r"^http(s)?://", argv[1]):
        print("URL should start with http[s]://")
        quit()

    parsed_url = urlparse(argv[1])
    netloc = parsed_url.netloc
    scheme = parsed_url.scheme
    if not netloc:
        print("Could not get netloc from url.")
        quit()
    
    if not scheme:
        scheme_netloc_sep = "//"
    else:
        scheme_netloc_sep = "://"
    
    query = " ".join(argv[2:]).lower()
    print('Scanning {} for "{}". This may take a while ...'.format(argv[1], query))
    start_time = time.time()
    
    scan_site(argv[1])

    end_time = time.time()
    print("Done! Took {} seconds.".format(end_time-start_time))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Keyboard interrupted")
