# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pykeyboard',
 'pyrogram_patch',
 'pyrogram_patch.fsm',
 'pyrogram_patch.fsm.storages',
 'pyrogram_patch.middlewares',
 'pyrogram_patch.middlewares.middleware_types',
 'pyrogram_patch.router',
 'pyrogram_patch.router.patched_decorators']

package_data = \
{'': ['*']}

install_requires = \
['kurigram>=2.1.35,<3.0.0']

setup_kwargs = {
    'name': 'kurigram-addons',
    'version': '0.1.0',
    'description': 'This package brings together several addons to kurigram including pykeyboard and FSM',
    'long_description': "<img align=center src=./logo.png length=80 width = 400>\n\n\n> This library is a collection of popular Addons and patches for pyrogram/Kurigram.\n> Currently, Pykeyboard and Pyrogram-patch have been added. You're welcome to add more.\n\n# Installation\n\n```shell\npip install kurigram-addons\n```\n\n# Usage\n\nPlease refer to specific readme.md for each addon.\n",
    'author': 'Johnnie',
    'author_email': '99084912+johnnie-610@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
