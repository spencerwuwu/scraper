Introduction
============

This is a firmware scraper that aims to download firmware images and associated
metadata from supported device vendor websites.

Dependencies
============
* [psycopg2](http://initd.org/psycopg/)
* [scrapy](http://scrapy.org/)

Usage
=====

* To run a specific scraper, e.g. `dlink`:

`scrapy crawl dlink`

* The result will be saved to `output/package.json

* To run all scrapers with maximum 4 in parallel, using [GNU Parallel](https://www.gnu.org/software/parallel/):

```parallel -j 4 scrapy crawl ::: `for i in ./firmware/spiders/*.py; do basename ${i%.*}; done` ```
