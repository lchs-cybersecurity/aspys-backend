from bs4 import BeautifulSoup
from tld import get_tld
from tld.utils import update_tld_names
import pandas as pd
import requests
import chardet
import re

print("Updating tlds...", end='\r')
update_tld_names()
print("Loading datasets...", end='\r')
safe_df = pd.read_csv("app/api/data/top10milliondomains.csv")
phish_df = pd.read_csv("app/api/data/verified_online.csv")
print("Done loading.")


# def make_phish_tlds():
#     tld_dict = {}
#     # total = 0
#     for i, row in phish_df.iterrows():
#         try:
#             tld = get_tld(row['url'])
#             tld_dict[tld] = tld_dict[tld]+1 if tld in tld_dict else 1
#             total += 1
#         except Exception as e:
#             pass
#     # print(total)
#     tld_df = pd.DataFrame({'tld': list(tld_dict.keys()), 'freq': list(tld_dict.values()) })
#     sorted_df = tld_df.sort_values(['freq'], ascending=[False])
#     sorted_df.to_csv('app/api/data/phishy_tlds.csv')

# make_phish_tlds()



def rate_email(content: str):
    """
    Returns tuple (score, reasons).
    Score is a value from 0.0 to 1.0 where 0.0 is no risk and 1.0 is a phish.
    Reasons is a list of strings.
    """
    links = set()
    soup = BeautifulSoup(content, "html.parser")
    for a in soup.find_all("a"):
        link = a.attrs.get("href")
        if link:
            links.add(link)
    worst_rating = 0.0
    worst_rating_reasons = []
    for link in links:
        (rating, reasons) = rate_link(link)
        if rating > worst_rating:
            worst_rating = rating
            worst_rating_reasons = reasons 
    return (worst_rating, worst_rating_reasons)


def rate_link(url: str):
    domain = get_domain(url)
    if is_top_domain(domain):
        return (0.0, ['in list of verified top domains'])
    elif is_reported_phish(url):
        return (1.0, ['in list of verified phishes'])
    else:
        return custom_rate_link(url)


def get_domain(url: str):
    tld = get_tld_object(url)
    if tld:
        domain = tld.parsed_url.netloc
        if domain.startswith("www."):
            domain = domain[4:]
        return domain


def get_tld_object(url: str):
    return get_tld(url, fix_protocol=True, fail_silently=True, as_object=True)


def is_top_domain(domain: str):
    safe_query = safe_df.query(f'Domain == "{domain}"')
    return len(safe_query) > 0


def is_reported_phish(url: str):
    phish_query = phish_df.query(f'url == "{url}"')
    return len(phish_query) > 0


def custom_rate_link(url: str):
    (score, red_flags) = score_url(url)

    (content_score, content_flags) = try_score_content(url)
    red_flags += content_flags
    if content_score >= 0:
        score = (score + content_score) / 2.0
   
    return (score, red_flags)


def score_url(url):
    """
    Feature                    Frequency
    ------------------------------------
    @ symbol in URL                 0.23
    IP based URL                    0.50
    URL with hexadecimal code       0.45
    Long URL length	                0.68
    Multiple slash in the URL path  0.82
    ------------------------------------
    Source: https://www.sciencedirect.com/science/article/pii/S1319157819304902
    """
    link_checks = {
        (0.23, '@ symbol in url', lambda a : '@' in a),
        (0.50, 'has ip in url', lambda a : contains_ip(a)),
        (0.45, 'has hexadecmial code in url', lambda a : contains_hex(a)),
        (0.68, 'long domain', lambda a : len(get_domain(a)) > 35),
        (0.82, 'multiple //s in path', lambda a : a.count('//') > 1)
    }
    red_flags = []
    for freq, name, check in link_checks:
        is_phishy = check(url)
        if is_phishy:
            red_flags.append(name)
    # TODO: calculate score with ml
    return (0.5, red_flags)


def try_score_content(url):
    content = try_get_content(url)
    if not content:
        return (-1, ['could not retrieve webpage content'])

    tld = get_tld_object(url)
    if tld:
        domain = tld.domain

    content_checks = {
        ('content not correlate with domain', lambda a : tld and not content_correlates(domain, content))
    }
    red_flags = []
    for name, check in content_checks:
        is_phishy = check(url)
        if is_phishy:
            red_flags.append(name)
    # TODO: calculate score with ml
    return (0.5, red_flags)
    

def try_get_content(url):
    try:
        res = requests.get(url)
        html = ''
        if res:
            res.encoding = chardet.detect(res.content)['encoding']
            return res.text
    except Exception as e:
        return None


def contains_ip(s):
    rx = re.compile('(([2][5][0-5]\.)|([2][0-4][0-9]\.)|([0-1]?[0-9]?[0-9]\.)){3}'+'(([2][5][0-5])|([2][0-4][0-9])|([0-1]?[0-9]?[0-9]))')
    match = rx.search(s)
    return match != None


def contains_hex(s):
    rx = re.compile('0[xX][0-9a-fA-F]+')
    match = rx.search(s)
    return match != None


def content_correlates(domain, content):
    rx = re.compile(normalize_text(domain), re.IGNORECASE)
    matches = re.findall(rx, normalize_text(content))
    return len(matches) > 1


def normalize_text(s):
    return re.sub(r"[-_\s]+", "", s, flags=re.UNICODE)
