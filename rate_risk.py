from bs4 import BeautifulSoup
from tld import get_tld
from tld.utils import update_tld_names
import pandas as pd
import requests

print('Updating...')
update_tld_names()
print('Loading datasets...')
safe_df = pd.read_csv('./data/top10milliondomains.csv')
phish_df = pd.read_csv('./data/verified_online.csv')
print('Done loading.')

def rate_email(content: str):
    '''
    Returns value 0.0 to 1.0 where
    0.0 is no risk and 1.0 is a phish.
    '''
    links = set()
    # soup = BeautifulSoup(content)
    soup = BeautifulSoup(content, 'html.parser')
    for a in soup.find_all('a'):
        link = a.attrs.get('href')
        if link:
            links.add(link)
    worst_rating = 0.0
    for link in links:
        rating = rate_link(link)
        if rating > worst_rating:
            worst_rating = rating
    return worst_rating

def rate_link(url: str):
    domain = get_domain(url)
    if is_top_domain(domain):
        return 0.0
    elif is_reported_phish(url):
        return 1.0
    else:
        return score_link(url)

def get_domain(url: str):
    tld = get_tld(url, fix_protocol=True, fail_silently=True, as_object=True)
    domain = tld.parsed_url.netloc
    if domain.startswith('www.'):
        domain = domain[4:]
    return domain

def is_top_domain(domain: str):
    safe_query = safe_df.query(f'Domain == "{domain}"')
    return len(safe_query) > 0

def is_reported_phish(url: str):
    phish_query = phish_df.query(f'url == "{url}"')
    return len(phish_query) > 0

def score_link(url: str):
    # TODO: implement basic phishiness scorer
    return 0.5