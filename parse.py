import csv
from bs4 import BeautifulSoup
import urllib2

def _get_site_html(url):
    """Read an html page with the right settings."""

    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Ge\cko)' 
        'Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

    try:
        req = urllib2.Request(url, headers = hdr)
        source = urllib2.urlopen(req).read()
    except:
        source = []

    return source

def _get_tree(url):
    """Parse an HTML page into a BeautifulSoup tree."""

    source = _get_site_html(url)
    try:
      tree = BeautifulSoup(source,'html.parser')
    except:
      tree = ''
    
    return tree
    
def _get_results(tree, year):
    """Parse results as tuples."""
    projects = []
    
    for t in tree.findAll('li', {'class': 'mdl-list__item mdl-list__item--one-line'}):   
        org = _clean(t.text)
        print org
        a = t.findChildren('a')[0]['href']
        org_url = 'https://www.google-melange.com' + a
        org_tree = _get_tree(org_url)

        for t1 in org_tree.findAll('span', {'class': 'mdl-list__item-primary-content'}):
            a1 = t1.findChildren('a')
            projs = [a['href'] for a in a1]

            for p in projs:
                proj_url = 'https://www.google-melange.com' + p
                proj_tree = _get_tree(proj_url)
                title = _clean(proj_tree.findAll('h3')[0].text)
                p = proj_tree.findAll('p')
                bio = _clean(p[0].text)
                student = bio.split('by')[-1].split('for')[0]
                description = _clean(p[1].text)
                projects.append((title, org, student, description))

    _save_results(projects, year)

def _clean(str):
    return str.replace('\n', '').replace("  ", "").encode("utf-8")


def _save_results(projects, year):

    titles = [p[0] for p in projects]
    descriptions = [p[1] for p in projects]
    students = [p[2] for p in projects]
    orgs = [p[3] for p in projects]
    rows = zip(titles, descriptions, students, orgs)

    with open('data/data'+year+'.csv', 'wb') as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow(row)

def parse(year):
    url = 'https://www.google-melange.com/archive/gsoc/' + year
    tree = _get_tree(url)
    _get_results(tree, year)

if __name__ == '__main__':
    parse('2015')
