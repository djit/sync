
import nltk
from bs4 import BeautifulSoup

def analyse(text):
    keywords = nltk.word_tokenize(text)
    return keywords
