import dataset

rdb = dataset.connect('sqlite:///reports.db')
bdb = dataset.connect('sqlite:///blacklists.db')
wdb = dataset.connect('sqlite:///whitelists.db')