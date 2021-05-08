import dataset
from flask import current_app as app

DB_IP = app.config['DB_IP']
DB_USER = app.config['DB_USER']
DB_PASS = app.config['DB_PASS']

rdb = dataset.connect(f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_IP}/reports')
bdb = dataset.connect(f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_IP}/blacklists')
wdb = dataset.connect(f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_IP}/whitelists')
tdb = dataset.connect(f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_IP}/testaddrlists')
ttdb = dataset.connect(f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_IP}/testtargetlists')
linktrackdb = dataset.connect(f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_IP}/linktracklists')
opentrackdb = dataset.connect(f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_IP}/opentracklists')
assessmentdb = dataset.connect(f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_IP}/assessments')

# def rdb():
#     return dataset.connect('sqlite:///reports.db')
# def bdb():
#     return dataset.connect('sqlite:///blacklists.db')
# def wdb():
#     return dataset.connect('sqlite:///whitelists.db')
# def tdb():
#     return dataset.connect('sqlite:///testaddrlists.db')
# def ttdb():
#     return dataset.connect('sqlite:///testtargetlists.db')
# def linktrackdb():
#     return dataset.connect('sqlite:///linktracklists.db')
# def opentrackdb():
#     return dataset.connect('sqlite:///opentracklists.db')
# def assessmentdb():
#     return dataset.connect('sqlite:///assessments.db')