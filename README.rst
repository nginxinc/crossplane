==========
crossplane
==========

|Build| |Release| |License| |Versions|

Reliable and fast NGINX configuration file parser and builder.

- `Install`_
- `Command Line Interface`_

  - `crossplane parse`_
  - `crossplane build`_
  - `crossplane lex`_
  - `crossplane format`_
  - `crossplane minify`_

- `Python Module`_

  - `crossplane.parse()`_
  - `crossplane.build()`_
  - `crossplane.lex()`_

- `Contributing`_

  - `Types of Contributions`_
  - `Get Started`_
  - `Pull Request Guidelines`_
  - `Tips`_


Install
=======

You can install both the `Command Line Interface`_ and `Python Module`_ via::

   pip install crossplane


Command Line Interface
======================

.. code-block::

   usage: crossplane <command> [options]

   various operations for nginx config files

   optional arguments:
     -h, --help            show this help message and exit

   commands:
     parse                 parses a json payload for an nginx config
     lex                   lexes tokens from an nginx config file
     minify                removes all whitespace from an nginx config
     format                formats an nginx config file
     help                  show help for commands


crossplane parse
----------------

This command will take a path to a main NGINX config file as input, then parse the entire config into
the schema defined below, and dumps the entire thing as a JSON payload.

.. code-block::

   usage: crossplane parse [-h] [-o OUT] [-i NUM] [--no-catch] [--tb-onerror]
                           filename

   parses a json payload for an nginx config

   positional arguments:
     filename              the nginx config file

   optional arguments:
     -h, --help            show this help message and exit
     -o OUT, --out OUT     write output to a file
     -i NUM, --indent NUM  number of spaces to indent output
     --ignore DIRECTIVES   ignore directives (comma-separated)
     --no-catch            only collect first error in file
     --tb-onerror          include tracebacks in config errors
     --single-file         do not include other config files
     --include-comments    include comments in json

**Privacy and Security**

Since ``crossplane`` is usually used to create payloads that are sent to different servers, it's important to keep security in mind. For that reason, the ``--ignore`` option was added. It can be used to keep certain sensitive directives out of the payload output entirely.

For example, we always the equivalent of this flag in the `NGINX Amplify Agent <https://github.com/nginxinc/nginx-amplify-agent/>`_ out of respect for our users' privacy::

   --ignore=auth_basic_user_file,secure_link_secret,ssl_certificate_key,ssl_client_certificate,ssl_password_file,ssl_stapling_file,ssl_trusted_certificate

Schema
~~~~~~

**Response Object**

.. code-block:: js

    {
        "status": String, // "ok" or "failed" if "errors" is not empty
        "errors": Array,  // aggregation of "errors" from Config objects
        "config": Array   // Array of Config objects
    }

**Config Object**

.. code-block:: js

    {
        "file": String,   // the full path of the config file
        "status": String, // "ok" or "failed" if errors is not empty array
        "errors": Array,  // Array of Error objects
        "parsed": Array   // Array of Directive objects
    }

**Directive Object**

.. code-block:: js

    {
        "directive": String, // the name of the directive
        "line": Number,      // integer line number the directive started on
        "args": Array,       // Array of String arguments
        "includes": Array,   // Array of integers (included iff this is an include directive)
        "block": Array       // Array of Directive Objects (included iff this is a block)
    }

.. note::

   If this is an ``include`` directive and the ``--single-file`` flag was not used, an ``"includes"`` value will be used that holds an Array of indices of the configs that are included by this directive.

   If this is a block directive, a ``"block"`` value will be used that holds an Array of more Directive Objects that define the block context.

**Error Object**

.. code-block:: js

    {
        "file": String,     // the full path of the config file
        "line": Number,     // integer line number the directive that caused the error
        "error": String,    // the error message
        "callback": Object  // only included iff an "onerror" function was passed to parse()
    }

.. note::

   If the ``--tb-onerror`` flag was used by crossplane parse, ``"callback"`` will contain a string that represents the traceback that the error caused.

Example
~~~~~~~

The main NGINX config file is at ``/etc/nginx/nginx.conf``:

.. code-block:: nginx

   events {
       worker_connections 1024;
   }

   http {
       include conf.d/*.conf;
   }

And this config file is at ``/etc/nginx/conf.d/servers.conf``:

.. code-block:: nginx

   server {
       listen 8080;
       location / {
           try_files 'foo bar' baz;
       }
   }

   server {
       listen 8081;
       location / {
           return 200 'success!';
       }
   }

So then if you run this::

   crossplane parse --indent=4 /etc/nginx/nginx.conf

The prettified JSON output would look like this:

.. code-block:: js

   {
       "status": "ok",
       "errors": [],
       "config": [
           {
               "file": "/etc/nginx/nginx.conf",
               "status": "ok",
               "errors": [],
               "parsed": [
                   {
                       "directive": "events",
                       "line": 1,
                       "args": [],
                       "block": [
                           {
                               "directive": "worker_connections",
                               "line": 2,
                               "args": [
                                   "1024"
                               ]
                           }
                       ]
                   },
                   {
                       "directive": "http",
                       "line": 5,
                       "args": [],
                       "block": [
                           {
                               "directive": "include",
                               "line": 6,
                               "args": [
                                   "conf.d/*.conf"
                               ],
                               "includes": [
                                   1
                               ]
                           }
                       ]
                   }
               ]
           },
           {
               "file": "/etc/nginx/conf.d/servers.conf",
               "status": "ok",
               "errors": [],
               "parsed": [
                   {
                       "directive": "server",
                       "line": 1,
                       "args": [],
                       "block": [
                           {
                               "directive": "listen",
                               "line": 2,
                               "args": [
                                   "8080"
                               ]
                           },
                           {
                               "directive": "location",
                               "line": 3,
                               "args": [
                                   "/"
                               ],
                               "block": [
                                   {
                                       "directive": "try_files",
                                       "line": 4,
                                       "args": [
                                           "foo bar",
                                           "baz"
                                       ]
                                   }
                               ]
                           }
                       ]
                   },
                   {
                       "directive": "server",
                       "line": 8,
                       "args": [],
                       "block": [
                           {
                               "directive": "listen",
                               "line": 9,
                               "args": [
                                   "8081"
                               ]
                           },
                           {
                               "directive": "location",
                               "line": 10,
                               "args": [
                                   "/"
                               ],
                               "block": [
                                   {
                                       "directive": "return",
                                       "line": 11,
                                       "args": [
                                           "200",
                                           "success!"
                                       ]
                                   }
                               ]
                           }
                       ]
                   }
               ]
           }
       ]
   }

crossplane parse (advanced)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This tool uses two flags that can change how ``crossplane`` handles errors.

The first, ``--no-catch``, can be used if you'd prefer that crossplane quit parsing after the first error it finds.

The second, ``--tb-onerror``, will add a ``"callback"`` key to all error objects in the JSON output, each containing
a string representation of the traceback that would have been raised by the parser if the exception had not been caught.
This can be useful for logging purposes.

crossplane build
----------------

This command will take a path to a file as input. The file should contain a JSON representation of an NGINX config that has
the structure defined above. Saving and using the output from ``crossplane parse`` to rebuild your config files should not
cause any differences in content except for the formatting.

.. code-block::

   usage: crossplane build [-h] [-d PATH] [-f] [-i NUM | -t] [--no-headers]
                           [--stdout] [-v]
                           filename

   builds an nginx config from a json payload

   positional arguments:
     filename              the file with the config payload

   optional arguments:
     -h, --help            show this help message and exit
     -v, --verbose         verbose output
     -d PATH, --dir PATH   the base directory to build in
     -f, --force           overwrite existing files
     -i NUM, --indent NUM  number of spaces to indent output
     -t, --tabs            indent with tabs instead of spaces
     --no-headers          do not write header to configs
     --stdout              write configs to stdout instead


crossplane lex
--------------

This command takes an NGINX config file, splits it into tokens by removing whitespace and comments, and dumps the list of tokens as a JSON array.

.. code-block::

   usage: crossplane lex [-h] [-o OUT] [-i NUM] [-n] filename

   lexes tokens from an nginx config file

   positional arguments:
     filename              the nginx config file

   optional arguments:
     -h, --help            show this help message and exit
     -o OUT, --out OUT     write output to a file
     -i NUM, --indent NUM  number of spaces to indent output
     -n, --line-numbers    include line numbers in json payload

Example
~~~~~~~

Passing in this NGINX config file at ``/etc/nginx/nginx.conf``:

.. code-block:: nginx

   events {
       worker_connections 1024;
   }

   http {
       include conf.d/*.conf;
   }

By running::

   crossplane lex /etc/nginx/nginx.conf

Will result in this JSON output:

.. code-block:: js

   ["events","{","worker_connections","1024",";","}","http","{","include","conf.d/*.conf",";","}"]

However, if you decide to use the ``--line-numbers`` flag, your output will look like:

.. code-block::

   [["events",1],["{",1],["worker_connections",2],["1024",2],[";",2],["}",3],["http",5],["{",5],["include",6],["conf.d/*.conf",6],[";",6],["}",7]]

crossplane format
-----------------

This is a quick and dirty tool that uses `crossplane parse`_ internally to format an NGINX config file.
Currently it removes all blank lines and comments, but this may get improved more in the future if there's
demand for it. As of now, it serves the purpose of demonstrating what you can do with ``crossplane``'s parsing abilities.

.. code-block::

   usage: crossplane format [-h] [-o OUT] [-i NUM | -t] filename

   formats an nginx config file

   positional arguments:
     filename              the nginx config file

   optional arguments:
     -h, --help            show this help message and exit
     -o OUT, --out OUT     write output to a file
     -i NUM, --indent NUM  number of spaces to indent output
     -t, --tabs            indent with tabs instead of spaces

crossplane minify
-----------------

This is a simple and fun little tool that uses `crossplane lex`_ internally to remove as much whitespace from
an NGINX config file as possible without affecting what it does. It can't imagine it will have much of a use to
most people, but it demonstrates the kinds of things you can do with ``crossplane``'s lexing abilities.

.. code-block::

   usage: crossplane minify [-h] [-o OUT] filename

   removes all whitespace from an nginx config

   positional arguments:
     filename           the nginx config file

   optional arguments:
     -h, --help         show this help message and exit
     -o OUT, --out OUT  write output to a file


Python Module
=============

In addition to the command line tool, you can import ``crossplane`` as a python module.
There are two basic functions that the module will provide you: ``parse`` and ``lex``.

crossplane.parse()
------------------

.. code-block:: python

   import crossplane
   payload = crossplane.parse('/etc/nginx/nginx.conf')

This will return the same payload as described in the `crossplane parse`_ section, except it will be
Python dicts and not one giant JSON string.

crossplane.build()
------------------

.. code-block:: python

   import crossplane
   config = crossplane.build(
       [{
           "directive": "events",
           "args": [],
           "block": [{
               "directive": "worker_connections",
               "args": ["1024"]
           }]
       }]
   )

This will return a single string that contains an entire NGINX config file.

crossplane.lex()
----------------

.. code-block:: python

   import crossplane
   tokens = crossplane.lex('/etc/nginx/nginx.conf')

``crossplane.lex`` generates 2-tuples. Inserting these pairs into a list will result in a long list similar
to what you can see in the `crossplane lex`_ section when the ``--line-numbers`` flag is used, except it
will obviously be a Python list of tuples and not one giant JSON string.


Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/nginxinc/crossplane/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug"
is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "feature"
is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

crossplane could always use more documentation, whether as part of the
official crossplane docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/nginxinc/crossplane/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions are welcome :)

Get Started
-----------

Ready to contribute? Here's how to set up `crossplane` for
local development.

#. Fork_ the `crossplane` repo on GitHub.
#. Clone your fork locally::

    git clone git@github.com:your_name_here/crossplane.git

#. Create a branch for local development::

    git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

#. When you're done making changes, check that your changes pass style and unit
   tests, including testing other Python versions with tox::

    tox

   To get tox, just pip install it.

#. Commit your changes and push your branch to GitHub::

    git add .
    git commit -m "Your detailed description of your changes."
    git push origin name-of-your-bugfix-or-feature

#. Submit a pull request through the GitHub website.

.. _Fork: https://github.com/nginxinc/crossplane/fork

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

#. The pull request should include tests.
#. The pull request should work for CPython 2.6, 2.7, 3.3, and 3.6, and for PyPy.
   Check https://travis-ci.org/nginxinc/crossplane under pull requests for
   active pull requests or run the ``tox`` command and make sure that the
   tests pass for all supported Python versions.
#. Make sure to add yourself to the Contributors list in AUTHORS.rst :)


.. #. If the pull request adds functionality, the docs should be updated. Put
      your new functionality into a function with a docstring, and add the
      feature to the list in README.rst.

Tips
----

To run a subset of tests::

    tox -e <env> -- tests/<file>[::test]

To run all the test environments in *parallel* (you need to ``pip install detox``)::

    detox

.. |Build| image:: https://img.shields.io/travis/nginxinc/crossplane/master.svg
   :target: https://travis-ci.org/nginxinc/crossplane

.. |Release| image:: https://img.shields.io/github/release/nginxinc/crossplane.svg
   :target: https://github.com/nginxinc/crossplane/releases

.. |License| image:: https://img.shields.io/pypi/l/crossplane.svg
   :target: https://pypi.python.org/pypi/crossplane

.. |Versions| image:: https://img.shields.io/pypi/pyversions/crossplane.svg
   :target: https://pypi.python.org/pypi/crossplane

