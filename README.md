# Shareholding

[![Build Status](https://travis-ci.org/johnbywater/es-example-shareholding.svg?branch=master)](https://travis-ci.org/johnbywater/es-example-shareholding)
[![Coverage Status](https://coveralls.io/repos/github/johnbywater/es-example-shareholding/badge.svg?branch=master)](https://coveralls.io/github/johnbywater/es-example-shareholding)

Example "shareholding" application using the Python eventsourcing library.

To use SQLAlchemy [persistence](https://eventsourcing.readthedocs.io/en/v9.2.20/topics/persistence.html), do something like:
```Shell
export PERSISTENCE_MODULE='eventsourcing_sqlalchemy'
export SQLALCHEMY_URL='sqlite:///:memory:'
```
