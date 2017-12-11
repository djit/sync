import pickle
import hashlib
import re
from slugify import slugify


# compute ranking index based on simple algorythm
def rank(data):
    ranking = 10.0

    # ranking stays at 10 if 10 pictures or more
    try:
        if data['pictures']:
            if len(data['pictures']) >= 10:
                ranking = 1*ranking
            else:
                ranking = len(data['pictures'])/10 * ranking
    except:
        ranking = ranking / 2
        pass

    # ranking stays at 10 if description text lenght > 1000 letters
    try:
        if data['description']:
            if len(data['description']) >= 1000:
                ranking = 1*ranking
            else:
                ranking = len(data['description'])/1000*ranking
    except:
        ranking = ranking / 2
        pass

    # ranking stays at 10 if at least 10 features listed
    try:
        if data['features']:
            if len(data['features']) >= 10:
                ranking = 1*ranking
            else:
                ranking = len(data['features'])/2*ranking
    except:
        ranking = ranking / 2
        pass

    # price is too low (price displayed per month and payment_type not stated as monthly)
    try:
        if data['payment_frequency']:
            if data['payment_frequency'] != 'month' and data['price'] < 20000:
                ranking = 0.1*ranking
    except:
        pass

    # size is not compatible with market rate for this kind of property
    if data['size']:
        if data['size'] > 0:
            if (data['price']/data['size']) < 40:
                ranking = 0.2*ranking
        else:
            ranking = 0.5*ranking
    else:
        ranking = 0.5*ranking

    return ranking


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


# build seo title for property
def seo_title(p):
    return p['data']['type'] + ' for ' + \
           p['data']['transaction_type'] + ' in ' + \
           p['data']['community']
           


# return SEF string
def sef(p):
    return slugify(seo_title(p))
