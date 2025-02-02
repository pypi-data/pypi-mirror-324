import pickle
import json
from collections import OrderedDict
from itertools import chain

def dedup_list(ls):
  return list(OrderedDict.fromkeys(ls))

def concat(ls):
  return list(chain.from_iterable(ls))

def read_json(fn):
  with open(fn) as f:
    return json.load(f)

def write_json(obj, fn):
  with open(fn, 'w') as f:
    json.dump(obj, f, indent=2)

def read_pickle(fn):
  with open(fn, 'rb') as f:
    return pickle.load(f)

def write_pickle(r, fn):
  with open(fn, 'wb') as f:
    pickle.dump(r, f)