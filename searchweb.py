#!/usr/bin/env python3

from html.parser import HTMLParser
from urllib.parse import urlparse
from sys import argv, stderr
import requests
import re


netloc = None
scheme = None
scheme_netloc_sep = None
query = None
curr_site = None
seen_sites = set()


class Parser(HTMLParser):
    
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for att in attrs:
                
                if att[0] != "href": 
                    continue

                if re.match(r"^http(s)?://", att[1]):
                    continue

                if att[1].startswith("mailto:"):
                    continue

                if re.match(r".+\.[a-zA-Z]{2,4}$", att[1]):  # we do not want to look at pdfs, pictures etc.
                    if not (att[1].endswith(".html") or att[1].endswith(".htm")): # we do, however, want to look at html data
                        #print("regex on {} matched. Skipping.".format(att[1]))
                        continue

                if "#" in att[1]:
                    # Strip it
                    idx = att[1].find("#")
                    att = att[0], att[1][:idx]

                if att[1].startswith("\\'") and att[1].endswith("\\'"):
                    s = att[1][2:-2]
                    att = att[0], s

                # print("Found subdomain: {}".format(att[1]))
                
                if len(att[1]) < 1:
                    continue

                # print(scheme, scheme_netloc_sep, netloc, att[1])
                if att[1][0] == "/":
                    new_site = scheme + scheme_netloc_sep + netloc + att[1]
                else:
                    new_site = scheme + scheme_netloc_sep + netloc + "/" + att[1]

                scan_site(new_site)

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        if query in data.lower():
            print("Found on {}".format(curr_site))


def scan_site(url):
    global curr_site
    #print("Scanning {}...".format(url), end="")
    if url in seen_sites:
        #print("Already seen.")
        return
    #print()

    curr_site = url
    seen_sites.add(url)

    pars = Parser()
    req = requests.get(url)
    try:
        html = req.content.decode("UTF-8")
    except UnicodeDecodeError:
        #print("Could not decode data from {}. It may be an image or document".format(url), file=stderr)
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
    scan_site(argv[1])



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Keyboard interrupted")
