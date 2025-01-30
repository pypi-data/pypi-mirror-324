# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['seamless_entropy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'seamless-entropy',
    'version': '0.1.0',
    'description': 'An experimental package intended to test adaptive dependencies for numeric code.',
    'long_description': '# Seamless entropy\n\nThe purpose of this package is to test and demonstrate how to create Python modules which can correctly fallback to supported functionality if dependencies such as C compilation, scipy, numba, etc., are not available.\n',
    'author': 'Jack Grahl',
    'author_email': 'jack.grahl@gmail.com',
    'maintainer': 'Jack Grahl',
    'maintainer_email': 'jack.grahl@gmail.com',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
