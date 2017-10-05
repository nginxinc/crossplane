==========
crossplane
==========

Reliable and fast NGINX configuration file parser.

- `Install`_
- `Scripts`_

  - `scripts/parse.py`_
  - `scripts/lex.py`_
  - `scripts/format.py`_
  - `scripts/minify.py`_

- `Contributing`_

  - `Types of Contributions`_
  - `Get Started`_
  - `Pull Request Guidelines`_
  - `Tips`_


Install
=======

.. code-block::

   pip install crossplane


Scripts
=======

There's a few different scripts that are included in this project.

Currently, the only way to run them is to clone this repository, but soon they will be
automatically installed when installing the package via pip.


scripts/parse.py
----------------

.. code-block::

   usage: parse.py [-h] [--no-catch] [--tb-onerror] [-i num] filename

   Prints a JSON payload for a given nginx config

   positional arguments:
     filename              the nginx config file to parse

   optional arguments:
     -h, --help            show this help message and exit
     --no-catch            only collect first error in file
     -i num, --indent num  number of spaces to indent output

Example
~~~~~~~

This nginx config is at ``/etc/nginx/nginx.conf``:

.. code-block:: nginx

   events {
       worker_connections 1024;
   }

   http {
       server {
           listen       127.0.0.1:8080;
           server_name  default_server;
           location / {
               try_files 'foo bar' baz;
           }
       }
   }

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
                 "args": ["1024"]
               }
             ]
           },
           {
             "directive": "http",
             "line": 5,
             "args": [],
             "block": [
               {
                 "directive": "server",
                 "line": 6,
                 "args": [],
                 "block": [
                   {
                     "directive": "listen",
                     "line": 7,
                     "args": ["127.0.0.1:8080"]
                   },
                   {
                     "directive": "server_name",
                     "line": 8,
                     "args": ["default_server"]
                   },
                   {
                     "directive": "location",
                     "line": 9,
                     "args": ["/"],
                     "block": [
                       {
                         "directive": "try_files",
                         "line": 10,
                         "args": ["foo bar", "baz"]
                       }
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
        "line": Integer,     // line number the directive started on
        "args": Array        // Array of String arguments
    }

.. note::

   If this is an ``include`` directive, an ``"includes"`` value will be used that holds an Array of paths to the configs that are included by this directive.

   If this is a block directive, a ``"block"`` value will be used that holds an Array of more Directive Objects that define the block context.


scripts/lex.py
--------------
*Documentation in progress.*

scripts/format.py
-----------------
*Documentation in progress.*

scripts/minify.py
-----------------
*Documentation in progress.*


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

    tox -e <env> -- py.test <test>

To run all the test environments in *parallel* (you need to ``pip install detox``)::

    detox


