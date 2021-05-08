import dataset
from flask import current_app as app

DB_IP = app.config['DB_IP']
DB_USER = app.config['DB_USER']
DB_PASS = app.config['DB_PASS']

rdb = dataset.connect(f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_IP}/reports', engine_kwargs={'pool_size': 20})
bdb = dataset.connect(f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_IP}/blacklists', engine_kwargs={'pool_size': 20})
wdb = dataset.connect(f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_IP}/whitelists', engine_kwargs={'pool_size': 20})
tdb = dataset.connect(f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_IP}/testaddrlists', engine_kwargs={'pool_size': 20})
ttdb = dataset.connect(f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_IP}/testtargetlists', engine_kwargs={'pool_size': 20})
linktrackdb = dataset.connect(f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_IP}/linktracklists', engine_kwargs={'pool_size': 20})
opentrackdb = dataset.connect(f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_IP}/opentracklists', engine_kwargs={'pool_size': 20})
assessmentdb = dataset.connect(f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_IP}/assessments', engine_kwargs={'pool_size': 20})

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