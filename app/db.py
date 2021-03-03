import dataset

def rdb():
    return dataset.connect('sqlite:///reports.db')
def bdb():
    return dataset.connect('sqlite:///blacklists.db')
def wdb():
    return dataset.connect('sqlite:///whitelists.db')
def tdb():
    return dataset.connect('sqlite:///testaddrlists.db')
def ttdb():
    return dataset.connect('sqlite:///testtargetlists.db')
def linktrackdb():
    return dataset.connect('sqlite:///linktracklists.db')
def opentrackdb():
    return dataset.connect('sqlite:///opentracklists.db')
def assessmentdb():
    return dataset.connect('sqlite:///assessments.db')