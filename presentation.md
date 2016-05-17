title: Searching documents with Apache Solr
author:
    name: Alex Volkov
    twitter: a_volkov
output: basic.html
controls: true

--

### Solr

* Makes it easy to develop search application.
* Built on Lucene
* Used by DucksDucksGo, Ticketmaster, Instagram and Netflix

--

### My Usecase

* Needed better search than Mezzanine CMS provices
* Needed an ability to search PDF and Word documents
* Used Django haystack as a frontend to Solr.
* Some works still needed to replace built-in search in Mezzaning

--

### Django Haystack Backends

* Elastic Search
* Whoosh
* Xapian

--

### Solr Server

Solr is built as a web service, running on Jetty web server,
On port 8983, with RESTful API with JSON responses.

--

### Solr Server (cont'd)

#### HAHA Gotcha

#### It's XML all the way down


--

### Solr Server (cont'd)

* PySolr -- A python library to interact with all the messy XML


--

### Solr Server (cont'd)

* Apache Tika -- used to be stand-alone project for document extraction, now a part of solr
* Documents can be indexed directly or extracted and indexed.


--

### Download and install Solr

```
$ wget http://apache.mirror.vexxhost.com/lucene/solr/5.3.1/solr-5.3.1.tgz
$ tar xzf solr-5.3.1.tgz
$ cd solr-5.3.1
```

--

### Start Solr in Schemaless mode

```
$ ./bin/solr start -e schemaless
```

Navigate with a browser to solr port, the page will show all kinds of stats.

--

### PySolr

Installation

```
$ pip install pysolr
```

Configuration

```
import pysolr

solr = pysolr.Solr(
    'http://localhost:8983/solr/gettingstarted',
    timeout=10
)
```

--

### Extracting data & indexing

```
with open('testfile.doc', 'rb') as fh:
    # only extract data
    data = solr.extract(fh, extract_only=True)
    content = extract_content(data['contents'])

    #prepare index

    index = [{
        'id': 'that_word_document',
        'title': content,
    }]

    solr.add(index)
```


--

### Searching

```
results = solr.search('indexed token')
```

Results contain a list of document ids/scores

--

### Deleting item from index

```
solr.delete=(id='that_word_document')
```

--

### Clearing index

```
solr.delete=(q='*:*')
```

--

### More examples

See solr_test.py

--