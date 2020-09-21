import dataset

def rdb():
    return dataset.connect('sqlite:///reports.db')
def bdb():
    return dataset.connect('sqlite:///blacklists.db')
def wdb():
    return dataset.connect('sqlite:///whitelists.db')