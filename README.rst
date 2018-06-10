Traverse JSON
============

|PyPI|
|Build Status|

A python library for accessing and searching JSON via
/slashed/paths

The package lets you traverse a JSON object as if it were a filesystem.
When traversing a dictionary, a string key or or a regular expression
pattern is used to traverse forward. When traversing a list, a string
representation of slicing index is used to traverse forward.

sdists are available on pypi: http://pypi.python.org/pypi/traverse_json

Installing
==========

The best way to install jsonTraverse is via easy\_install or pip.

::

    pip install traverse_json

Using jsonTraverse
===================

.. code-block:: python

    import jsonTraverse

Separators
==========

The character that should separate path components. The default is '/',
but you can set it to whatever you want.

Searching JSON file
===================

Suppose we have a JSON like this:

.. code-block:: python

    programmers = [
      {
        "name": "Aaron",
        "age": 21,
        "language": ["Java", "Python"]
      },
      {
        "name": "Bob",
        "age": 36,
        "language": ["C++", "Java"]
      },
      {
        "name": "Charles",
        "age": 50,
        "language": ["C++", "Fortran"]
      },
      {
        "name": "David",
        "age": 18,
        "language": ["Python"]
      },
      {
        "name": "Liam",
        "age": 42,
        "language": ["C", "Java"]
      },
      {
        "name": "Sam",
        "age": 28,
        "language": ["Java", "Python"]
      }
    ]

Now we want to create a list of age of all the programmers. Here is
the approach we can use with `traverse_json` package.

.. code-block:: pycon

    >>> import traverse_json
    >>> json_obj = traverse_json.JsonTraverse(json_data=programmers)
    >>> path_to_age = ':/age'
    >>> ages = json_obj.traverse(path_to_age, named=False)


That was really easy. A harder question is to find out the most popular
programming language among programmers under 35 and above 35. Here is the
approach we can use with `traverse_json` package.

.. code-block:: pycon

    >>> from six import iteritems
    >>> ages = json_obj.traverse(path_to_age, named=True)
    >>> paths_to_under_35 = [
          '/'.join(path.split('/')[:-1] + ['language'])
          for path, age in iteritems(ages) if age < 35
        ]
    >>> paths_to_above_35 = [
          '/'.join(path.split('/')[:-1] + ['language'])
          for path, age in iteritems(ages) if age >= 35
        ]
    >>> lang_under_35 = [
          lang
          for path in paths_to_under_35
          for lang in json_obj.traverse(path, named=False)[0]
        ]
    >>> lang_above_35 = [
          lang
          for path in paths_to_above_35
          for lang in json_obj.traverse(path, named=False)[0]
        ]
    >>> print(max(lang_under_35, key=lang_under_35.count))
    >>> print(max(lang_above_35, key=lang_above_35.count))


Loading JSON
============

In the above example, we demonstrated loading JSON object directly.
Besides, we can also load JSON from a file or from a URL. Examples
are given below

.. code-block:: pycon

    >>> import traverse_json
    >>> json_file = traverse_json.JsonTraverse(filepath=filepath)
    >>> json_url = traverse_json.JsonTraverse(url=url)


Contact
=======
If you have any questions or encounter any bugs, please contact the author (Feiyang Niu, statech.forums@gmail.com)
