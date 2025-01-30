# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['seamless_entropy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'seamless-entropy',
    'version': '0.2.3',
    'description': 'An experimental package intended to test adaptive dependencies for numeric code.',
    'long_description': "# Seamless entropy\n\nThe purpose of this package is to test and demonstrate how to create Python modules which can correctly fallback to supported functionality if dependencies such as C compilation, scipy, numba, etc., are not available.\n\nThis packages exports a single function, `binary_entropy`, which returns the entropy of a probability, expressed in bits (rather than using the natural logarithm, as is customary in most mathematical applications).\n\n```\n>>> from seamless_entropy import binary_entropy\n>>> binary_entropy(0.25)\n0.5\n\n```\n\n## Choosing an implementation\nThe package will choose from one of several implementations of this function, depending on the environment \n\n a. at build time, and \n b. at run time.\n\nFor example, if C compilation is supported and enabled, either when building a wheel, or when installing from source, an implementation in a C extension module will be built and used in preference.\n\nIf numba is present, either because the package was installed as `seamless_entropy[numba]`, or because it happened to be installed anyway, the Python function will be jitted before use.\n\nIf scipy is present, again either by installing `seamless_entropy[scipy]` or incidentally, an implementation which calls a scipy function will be preferred.\n\n## Controlling the build\nWhen building (this can mean either building a redistributable wheel, or installing from source), you can set environment variables to control how the package is built.\n\n- DISABLE_SPEEDUPS: setting this to '1' means that C code will not be built even if that is supported.\n- REQUIRE_SPEEDUPS: setting this to '1' means that if C code cannot be built, the \n\n## TODO\nIt would be nice to have a Cython implementation. Note that Cython support depends on C support; if Cython is available than native C should work, but not the converse. Thus the Cython implementation should take priority over the C one.\n\nHow about configurable order of preference for different platforms?\n\n## Installation errors\nThe aim with this package is to solve in one place all the packaging issues which arise from a package which optionally includes faster and more efficient versions. This technology is intended to be re-used in other packages. It would be nice to make this package as robust as possible on various Python platforms. If you encounter any problems installing or running this package, on any Python setup no matter how weird, please let me know! I would love to know about your environment so that I can make this package work on it.",
    'author': 'Jack Grahl',
    'author_email': 'jack.grahl@gmail.com',
    'maintainer': 'Jack Grahl',
    'maintainer_email': 'jack.grahl@gmail.com',
    'url': 'https://github.com/jwg4/seamless_entropy',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
