import nltk
import spacy
import sklearn
import pandas as pd
import numpy as np


print("He")

print(f"NLTK version: {nltk.__version__}")
print(f"spaCy version: {spacy.__version__}")
print(f"scikit-learn version: {sklearn.__version__}")

nlp = spacy.load("en_core_web_sm")
doc = nlp("Hello, world!")
print(f"spaCy model loaded: {nlp.meta['name']}")