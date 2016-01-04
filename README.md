Searching documents with Apache Solr
==================

# Background

Solr makes it easy for programmers to develop sophisticated, high-performance search application.


Solr builds on another open source search technology: [Lucene](https://lucene.apache.org/core/), a java library that provides indexing and search technology, spellchecking hit highlighting and advanced analysis/tokenization capabilities.


Another technology has been incorporated into Solr -- Apache Tika.
The [Apache Tika](https://tika.apache.org/) toolkit detects and extracts metadata and text from over a thousand different file types such as PPT, XLS and PDF.


# Why Solr?

I worked on a project that's been using Mezzanine CMS and it's built-in search was not great -- basically wide SQL queries on the database.
So I looked for something that does search better, and especially searches through Word and PDF documents.

Django Haystack is a universal search frontend for Django. Although some work was still needed to replace built-in search in Mezzanine.
Django Haystack has the following alternative backends:

Elastic search -- also built on Lucene, but more about big data than general-purpose searching.
Whoosh -- Indexing and search library implemented in python, but provides no document extraction
Xapian -- A C++ search engine library with bindings in every language including python

# How solr interacts with python?

Solr is built as a web service, running on  [Jetty](http://www.eclipse.org/jetty/) web server, usually on port 8983, exposing XMLRPC interface for other applications.

Good news, you wouldn't have to deal with XML RPC because there's already pysolr that does it for you.

[PySolr PyPi](https://pypi.python.org/pypi/pysolr/3.3.3)
[PySolr Github](https://github.com/toastdriven/pysolr)

Django Haystack uses pySolr as a way of communicating with solr.

# Quickstart

