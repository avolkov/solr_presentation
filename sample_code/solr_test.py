#!/usr/bin/env python3
import pysolr
import re
import os

from bs4 import BeautifulSoup


DST_PATH = '../sample_documents/'
file_ext = [re.compile(x, re.IGNORECASE) for x in ("[.]doc$", "[.]pdf$", )]


def is_document(in_fname):
    for fe in file_ext:
        if fe.search(in_fname):
            return True
    return False


def build_dict(in_path):
    out = {}
    for path, _, files in os.walk(in_path):
        for f in files:
            if is_document(f):
                out[f.lower()] = os.path.join(path, f)
    return out


def str_rep(in_str):
        in_str = in_str.replace("\n", '')
        out_str = re.sub('\s+', ' ', in_str)
        out_str = re.sub("[.]+", '', out_str)
        return out_str


def extract_content(solr_data):

    soup = BeautifulSoup(solr_data, "html5lib")
    out = [str_rep(x) for x in soup.stripped_strings]
    return " ".join(out)

solr = pysolr.Solr(
    'http://localhost:8983/solr/gettingstarted',
    timeout=10
)

solr.delete(q='*:*')
for key, val in build_dict(DST_PATH).items():
    with open(val, 'rb') as fh:
        try:
            data = solr.extract(fh, extractOnly=True)
        except pysolr.SolrError as e:
            print("Damaged file %s" % val)
            continue
        metadata = data['metadata']
        content = extract_content(data['contents'])
        index = [{
            'id': key,
            '_text_': content
        }]
        solr.add(index)

#res = solr.search("test")
