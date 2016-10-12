import time
import urllib2
from bs4 import BeautifulSoup

def get_site_html(url):
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

def get_tree(url):
    """Parse an HTML page into a BeautifulSoup tree."""

    source = get_site_html(url)
    try:
      tree = BeautifulSoup(source,'html.parser')
    except:
      tree = ''
    
    return tree
    
def get_results(tree):
    
    projects = []
    
    for t in tree.findAll('li', {'class': 'mdl-list__item mdl-list__item--one-line'}):
        org = t.text.replace('\n', '')
        a = t.findChildren('a')[0]['href']
        org_url = 'https://www.google-melange.com' + a
        org_tree = get_tree(org_url)

        for t1 in org_tree.findAll('span', {'class': 'mdl-list__item-primary-content'}):
            a1 = t1.findChildren('a')
            projs = [a['href'] for a in a1]

            for p in projs:
                proj_url = 'https://www.google-melange.com' + p
                proj_tree = get_tree(proj_url)
                title = proj_tree.findAll('h3')[0]
                p = proj_tree.findAll('p')
                bio = p[0].text.replace('\n', '')
                description = p[1].text.replace('\n', '')
                student = bio.split('by')[-1].split('for')[0].replace("  ", "")
                description = description.replace("  ", "")

                projects.append((title, description, student, org))

    return projects

def save_results(projects):

    pass
            
def main():
    url = 'https://www.google-melange.com/archive/gsoc/2015'
    tree = get_tree(url)
    get_results(tree)

if __name__ == '__main__':
    main()
