from .models import Docs
import os
import Levenshtein
import json
import re
import numpy as np
import csv
from collections import defaultdict
from collections import Counter
import math
import pandas as pd

def read_file(n):
  path = Docs.objects.get(id = n).address;
  file = open(path)
  transcripts = json.load(file)
  return transcripts

def read_csv(n):
  path = Docs.objects.get(id=n).address;
  file = open(path)
  print("file has been opened")
  #transcripts = csv.reader(file,delimiter=",")
  #transcripts = list(transcripts)
  transcripts = pd.read_csv(file)
  print("file has been loaded")
  return transcripts


def tokenize(text):

  tokenized_text = text.lower()
  tokenized_text = re.findall(r'[a-z0-9]+',
                tokenized_text)  # splits string with delimiter being everything except alphabetical letters
  return tokenized_text