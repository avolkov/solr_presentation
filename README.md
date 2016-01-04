Searching documents with Apache Solr
==================

# Background

Solr makes it easy for programmers to develop sophisticated, high-performance search application.

Solr builds on another open source search technology: [Lucene](https://lucene.apache.org/core/), a java library that provides indexing and search technology, spellchecking hit highlighting and advanced analysis/tokenization capabilities.

Solr is used by DucksDucsGo, Ticketmaster, Instagram and Netflix.

Another technology has been incorporated into Solr -- Apache Tika.
The [Apache Tika](https://tika.apache.org/) toolkit detects and extracts metadata and text from over a thousand different file types such as PPT, XLS and PDF.


# Why Solr? My usecase.

I worked on a project that's been using Mezzanine CMS and it's built-in search was not great -- basically wide SQL queries on the database.
So I looked for something that does search better, and especially searches through Word and PDF documents.

Django Haystack is a universal search frontend for Django. Although some work was still needed to replace built-in search in Mezzanine.

Django Haystack has the following alternative backends:

Elastic search -- also built on Lucene, but more about big data than general-purpose searching.

Whoosh -- Indexing and search library implemented in python, but provides no document extraction

Xapian -- A C++ search engine library with bindings in every language including python

Although no alternative search backend provides document extraction support, in the end this wasn't as critical as it is possible to extract document content with Apache Tika, and then pass it to any indexing and searching backend.

# How solr interacts with python?

Solr is built as a web service, running on  [Jetty](http://www.eclipse.org/jetty/) web server, usually on port 8983, exposing XMLRPC interface for other applications.

Good news, you wouldn't have to deal with XML RPC because there's already pysolr that does it for you.

[PySolr PyPi](https://pypi.python.org/pypi/pysolr/3.3.3)
[PySolr Github](https://github.com/toastdriven/pysolr)

Django Haystack uses pySolr as a way of communicating with Solr.

# Quickstart

See solr_test.py for code example.

Here I'm going to start up solar with the default configuration, connect to it using pysolr, then extract file content using built in Apache Tika.

## Solr default setup

System requirements -- Java 1.7 or newer, Python 2.7 or 3.x. Apache Ant and Apache Ivy in case you want to build solr from source.

Download and extract solr

    $ wget http://apache.mirror.vexxhost.com/lucene/solr/5.3.1/solr-5.3.1.tgz
    $ tar xzf solr-5.3.1.tgz
    $ cd solr-5.3.1

Start solr in [schemaless mode](https://cwiki.apache.org/confluence/display/solr/Schemaless+Mode)


    $ ./bin/solr start -e schemaless

When solr starts up successfully something like the following will show up.


![Solr startup](screens/0001-solr-startup.png)

Navigate with a browser to solr port, the page will show all kinds of stats.

![Solr dashboard](screens/0002-solr-dashboard.png)

## Using PySolr

#### Install

    $ pip install pysolr

Connecting to solr

    import pysolr

    solr = pysolr.Solr(
        'http://localhost:8983/solr/gettingstarted',
        timeout=10
    )

#### Index

Indexing documents, first create a file handle to a document, then pass it to solr.

    with open('testfile.doc', 'rb') as fh:
        data = solr.extract(fh)

If you don't want to associate data with that particular filename, or some preprocessing is needed before inserting the data into the index, it is possible to opt out of direct indexing the file and just extracting the data.

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

Data is a dictionary with the following keys

*contents* -- contents of the file, usually some form of raw HTML or XML

*metada* -- document information like the following

    {'modified': ['2014-07-14T15:25:39Z'], 'dcterms:modified': ['2014-07-14T15:25:39Z'], 'Last-Modified': ['2014-07-14T15:25:39Z'], 'stream_source_info': ['file'], 'stream_size': ['859566'], 'created': ['Wed Jul 09 19:37:35 UTC 2014'], 'Content-Type': ['application/pdf'], 'Creation-Date': ['2014-07-09T19:37:35Z'], 'Last-Save-Date': ['2014-07-14T15:25:39Z'], 'pdf:encrypted': ['false'], 'X-Parsed-By': ['org.apache.tika.parser.DefaultParser', 'org.apache.tika.parser.pdf.PDFParser'], 'dc:format': ['application/pdf; version=1.4'], 'dcterms:created': ['2014-07-09T19:37:35Z'], 'pdf:PDFVersion': ['1.4'], 'meta:creation-date': ['2014-07-09T19:37:35Z'], 'xmpTPg:NPages': ['135'], 'stream_name': ['../sample_documents/HP40-102-2014-eng.pdf'], 'date': ['2014-07-14T15:25:39Z'], 'meta:save-date': ['2014-07-14T15:25:39Z']}

*responseHeader* -- solr response metrics

    {'status': 0, 'QTime': 2440}

I use beautiful soup to strip all XML information from the file and pass raw text data to indexer.

#### Search

    results = solr.search('indexed token')


#### Delete

Single index

    solr.delete=(id='that_word_document')

Clearing indexes

    solr.delete=(q='*:*')

### Live demo.

Example documents -- publications.gc.ca
See [solr_test.py](sample_code/solr_test.py)


# Setting up Django Haystack

Since version 5.x Solr switched to having live schema configuration from older XML mode, however Django Haystack doesn't support that yet, schema needs to be manually built from existing django models.

## Configuring Django

In settings.py

Add 'haystack in INSTALLED_APPS'

    INSTALLED_APPS = (
        ...
        'haystack',
        ...
    )

Define haystack cnnection:

    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
            'URL': 'http://localhost:8983/solr/haystack_core'
        }
    }


## Wiring up Django models


Add search indexes model in `<app_name>/search_indexes.py`

    from haystack import indexes
    from .models import SampleModel

    class SampleModelIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return FormFiles


In templates directory add search templates file `templates/search/indexes/<app_name>/<model_name>_text.txt`
The contents of the search template, would look much like regular template. Object variable is taken from an instance of a model returned by `get_model`in

      {{ object.title }}
      {{ object.description }}
      {{ object.version_date| date:"F j, Y" }}
      {{ object.document_data}}

Add document data extractor to SampleModel in `models.py`


Imports

    import pysolr
    from django.db import models
    from django.conf import settings
    ...

File data extractor

    def extract_files(solr_driver, file_paths):
        for f_path in file_paths:
            try:
                with open(f_path, 'rb') as fd:
                    try:
                        data = solr_driver.extract(fd, extractOnly=True)
                        yield extract_content(data['contents'])
                    except pysolr.SolrError:
                        pass
            except FileNotFoundError:
                pass

Model with a document property -- used for getting text extracted from the documents.

    class SampleModel(models.Model):
        ...model definitions...


        @property
        def document_data(self):
            """Return document content for Pdf and Word documents"""
            solr = pysolr.Solr(
                settings.HAYSTACK_CONNECTIONS['default']['URL'],
                timeout=TIMEOUT
            )
            return " ".join([x for x in extract_files(solr, self.files)])


## Generating Solr Schema from Django Haystack.

Copy solr xml from [Solr 5 for Django Haystack page](https://github.com/nazariyg/Solr-5-for-django-haystack/blob/master/solr.xml) to django-haystack project directory `/templates/search_configuration/solr.xml`

Generate a schema to be used with solr with the following command

       $ python manage.py build_solr_shema > schema.xml

Start solr server without initiating any example configurations.

    $ bin/solr start

Create brand-new configuration based on schema.xml, the one like that is called `basic_configs`
see [this blog post on finding solr home directory](http://blog.outerthoughts.com/2015/11/oh-solr-home-where-art-thou/) and [an answer on stackoverflow](http://stackoverflow.com/questions/33835385/solr-5-3-1-verifying-that-schema-xml-is-loaded)

     $ bin/solr create_core -d basic_configs -c haystack_core


Go to a newly created `haystack_core` directory under `solr/server/solr/haystack_core` replace existing `schema.xml` with the one generated by django_haystack with `build_solr_schema`.

In that directory create [core.properties file](https://cwiki.apache.org/confluence/display/solr/Moving+to+the+New+solr.xml+Format) with a content that looks similar to the following:


    #Written by CorePropertiesLocator
    #Mon Nov 23 19:51:29 UTC 2015
    name=haystack_core
    shard=${shard:}
    collection=${collection:haystack_core}
    config=${solrconfig:solrconfig.xml}
    schema=${schema:schema.xml}
    coreNodeName=${coreNodeName:}

Restart solr:

    $ bin/solr stop
    $ bin/solr start

Reindex everything:

    $ python manage.py rebuild_index


# Common pitfalls

Document text extraction may no longer works because it's not in basic_configs `solrconfig.xml` in `solr/server/solr/haystack_core`  generated by `create_core` command

Add the following to `solrconfig.xml`

    <requestHandler name="/update/extract"
                  startup="lazy"
                  class="solr.extraction.ExtractingRequestHandler" >
        <lst name="defaults">
            <str name="lowernames">true</str>
            <str name="uprefix">ignored_</str>

            <!-- capture link hrefs but ignore div attributes -->
            <str name="captureAttr">true</str>
            <str name="fmap.a">links</str>
            <str name="fmap.div">ignored_</str>
        </lst>
    </requestHandler>

This will cause an error with the message that begins like the following:

    Error loading class 'solr.extraction.ExtractingRequestHandler'


From example/files/conf/solrconfig.xml, add the following libraries under `<luceneMatchVersion>5.2.0</luceneMatchVersion>`

    <lib dir="${solr.install.dir:../../../..}/contrib/extraction/lib" regex=".*\.jar" />
    <lib dir="${solr.install.dir:../../../..}/contrib/dataimporthandler/lib/" regex=".*\.jar" />
    <lib dir="${solr.install.dir:../../../..}/dist/" regex="solr-dataimporthandler-.*\.jar" />

    <lib dir="${solr.install.dir:../../../..}/contrib/extraction/lib" regex=".*\.jar" />
    <lib dir="${solr.install.dir:../../../..}/dist/" regex="solr-cell-\d.*\.jar" />
    <lib dir="${solr.install.dir:../../../..}/contrib/clustering/lib/" regex=".*\.jar" />
    <lib dir="${solr.install.dir:../../../..}/dist/" regex="solr-clustering-\d.*\.jar" />
    <lib dir="${solr.install.dir:../../../..}/contrib/langid/lib/" regex=".*\.jar" />
    <lib dir="${solr.install.dir:../../../..}/dist/" regex="solr-langid-\d.*\.jar" />
    <lib dir="${solr.install.dir:../../../..}/contrib/velocity/lib" regex=".*\.jar" />
    <lib dir="${solr.install.dir:../../../..}/dist/" regex="solr-velocity-\d.*\.jar" />


# Solr Debugging

In case weird communication errors in solr appear, insert pdb statement in `/lib/python/site-packages/pysolr.py` on line 444, just before the following statement.

    if response.startswith('<?xml'):
            # Try a strict XML parse
            try:
            ....


This usually means that instead of an xml query response, an HTTP error response has occurred.
Print out the response:

    ipdb> print(response)
    b'<?xml version="1.0" encoding="UTF-8"?>\n<response>\n<lst name="responseHeader"><int name="status">400</int><int name="QTime">5</int></lst><lst name="error"><str name="msg">Exception writing document id hp40-104-2014-eng.pdf to the index; possible analysis error.</str><int name="code">400</int></lst>\n</response>\n'

Something has gone wrong with solr -- go into solr console and check logging pane:

![Solr logging pane](screens/099-solr-logging.png)

The actual error was:

    java.lang.IllegalArgumentException: Document contains at least one immense term in field="title" (whose UTF8 encoding is longer than the max length 32766), all of which were skipped.  Please correct the analyzer to not produce such terms.  The prefix of the first immense term is: '[80, 32, 82, 32, 79, 32, 84, 32, 69, 32, 67, 32, 84, 32, 73, 32, 78, 32, 71, 32, 67, 32, 65, 32, 78, 32, 65, 32, 68, 32]...', original message


# END

And as always... Happy Searching!
