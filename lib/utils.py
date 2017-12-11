import pickle
import hashlib
import re
from slugify import slugify


# strim html tags from string
def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)


# modifed urlretieve to add headers fields
def urlretrieve(urlfile, fpath):
    try:
        chunk = 4096
        f = open(fpath, "w")
        while 1:
            data = urlfile.read(chunk)
            if not data:
                break
            f.write(data.decode())
    except:
        return


# calculate input checksum
def checksum(input):
    return hashlib.md5(input).hexdigest()
