# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gocardless_to_csv']

package_data = \
{'': ['*']}

install_requires = \
['nordigen>=1.4.1', 'pyfzf>=0.3.1']

setup_kwargs = {
    'name': 'gocardless-to-csv',
    'version': '0.5.0',
    'description': 'Client for GoCardless Bank Data API that pulls transaction history and converts it to CSV',
    'long_description': None,
    'author': 'Dmitry Astapov',
    'author_email': 'dastapov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/adept/gocardless-to-csv',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
