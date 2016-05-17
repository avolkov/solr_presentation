title: Searching documents with Apache Solr
author:
    name: Alex Volkov
    twitter: a_volkov
output: basic.html
controls: true

--

# Solr

* Makes it easy to develop search application.
* Built on Lucene
* Used by DucksDucksGo, Ticketmaster, Instagram and Netflix

--

# My Usecase

* Needed better search than Mezzanine CMS provices
* Needed an ability to search PDF and Word documents
* Used Django haystack as a frontend to Solr.
* Some works still needed to replace built-in search in Mezzaning

--

# Django Haystack Backends

* Elastic Search
* Whoos
* Xapian

--

# Solr Server

Solr is built as a web service, running on Jetty web server,
On port 8983, with RESTful API with JSON responses.

--

# Solr Server (cont'd)

## HAHA Gotcha

## It's XML all the way down


--

# Solr Server (cont'd)

* PySolr -- A python library to interact with all the messy XML


--

# Solr Server (cont'd)

* Apache Tika -- used to be stand-alone project for document extraction, now a part of solr
* Documents can be indexed directly or extracted and indexed.


--