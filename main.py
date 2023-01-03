import datetime

import requests
from bs4 import BeautifulSoup


now = datetime.datetime.now().strftime("%Y-%m-%d")
website = 'https://rootandbloom.studio'
base_url = website
if website.endswith('/'):
    base_url = website[:-1]

scanned = []


def clean(a_elements):
    links = []
    skip_links = []
    for a in a_elements:
        link = a['href']

        if 'target' in a and a['target'] == '_blank':
            skip_links.append(link)
            continue

        if '#' in link or 'mailto:' in link or 'whatsapp:' in link or link == '/':
            skip_links.append(link)
            continue

        if link.startswith('/'):
            link = '{}{}'.format(base_url, link)

        if link.startswith('http://') is not True and link.startswith('https://') is not True:
            link = '{}/{}'.format(base_url, link)

        if link.startswith(base_url) is False:
            continue

        if link not in links:
            links.append(link)

    return [links, skip_links]


def get_next_scan_urls(urls):
    links = []
    for u in urls:
        if u not in scanned:
            links.append(u)
    return links


def scan(url):
    if url in scanned:
        return scanned

    print('Scan url: {}'.format(url))
    scanned.append(url)
    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html5lib')
    a_elements = soup.find_all('a', href=True)
    links, skip_links = clean(a_elements)

    next_scan_urls = get_next_scan_urls(links)
    print('Count next scan: {}'.format(len(next_scan_urls)))

    if len(next_scan_urls) != 0:
        for page in next_scan_urls:
            scan(page)

    return scanned


def main():
    urls = ''
    links = scan(website)
    print("total: %s" % len(links))

    for link in links:
        urls += f"""<url><loc>{link}</loc><lastmod>{now}</lastmod></url>"""

    xml = f"""<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>"""

    f = open('sitemap.xml', 'w')
    f.write(xml)
    f.close()


if __name__ == '__main__':
    main()
