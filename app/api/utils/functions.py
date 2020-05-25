from datetime import datetime, timedelta
import pytz

def now():
    return datetime.now(pytz.utc)

def limit_str(str, chars):
    return str[:chars-3] + (str[chars-3:] and "...")
