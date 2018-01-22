# -*- coding: utf-8 -*-
from .parser import parse
from .lexer import lex
from .builder import build

__all__ = ['parse', 'lex', 'build']

__title__ = 'crossplane'
__summary__ = 'Reliable and fast NGINX configuration file parser.'
__url__ = 'https://github.com/nginxinc/crossplane'

__version__ = '0.2.0'

__author__ = 'Arie van Luttikhuizen'
__email__ = 'aluttik@gmail.com'

__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2017 NGINX, Inc.'
