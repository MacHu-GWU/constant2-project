#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = "0.0.10"
__short_description__ = "Extendable json encode/decode library."
__license__ = "MIT"
__author__ = "Sanhe Hu"
__author_email__ = "husanhe@gmail.com"
__maintainer__ = "Sanhe Hu"
__maintainer_email__ = "husanhe@gmail.com"
__github_username__ = "MacHu-GWU"


try:
    from ._superjson import SuperJson, get_class_name, superjson as json
except Exception as e:  # pragma: no cover
    pass
