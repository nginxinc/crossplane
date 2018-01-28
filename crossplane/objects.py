# -*- coding: utf-8 -*-
from .parser import parse


#
# Functions
#

def _init_directive(directive_json):
    return NGXBlockDirective(**directive_json) if 'block' in directive_json \
        else NGXDirective(**directive_json)


#
# Classes
#

class NGXDirective(object):
    __slots__ = ('directive', 'line', 'args', 'includes')

    def __init__(self, directive='', line=0, args=[], includes=[], **kwargs):
        self.directive = directive
        self.line = line
        self.args = args
        self.includes = []

    def dict(self):
        return {
            slot: getattr(self, slot)
            for slot in self.__slots__
        }


class NGXBlockDirective(NGXDirective):
    __slots__ = ('index', 'directive', 'line', 'args', 'block')

    def __init__(self, block=[], **kwargs):
        super(NGXBlockDirective, self).__init__(**kwargs)
        self.index = {}
        self.block = block

        self._setup_block()

    def _setup_block(self):
        directives = []
        for directive_json in self.block:
            directives.append(_init_directive(directive_json))
            self.__index(directives[-1])

        self.block = directives

    def __index(self, directive):
        idx = self.index.get(directive.directive, [])
        idx.append(directive)
        self.index[directive.directive] = idx

    def __contains__(self, item):
        return item in self.index

    def __getattr__(self, name):
        if name in self.index:
            return self.get(name)
        else:
            raise AttributeError(
                '"{0s}" has not attribute "{1s}"'.format(
                    self.__class__.__name__,
                    name
                )
            )

    def get(self, directive):
        return self.index[directive] if directive in self.index else []

    def dict(self):
        dict_repr = {
            slot: getattr(self, slot)
            for slot in self.__slots__ if slot not in ('index', 'block')
        }

        dict_repr['block'] = [
            directive.dict() for directive in self.block
        ]

        return dict_repr


class NGXConfigFile(object):
    __slots__ = ('index', 'file', 'parsed')

    def __init__(self, file='', parsed=[], **kwargs):
        self.index = {}
        self.file = file
        self.parsed = parsed

        self._setup_parsed()

    def _setup_parsed(self):
        directives = []
        for directive_json in self.parsed:
            directives.append(_init_directive(directive_json))
            self.__index(directives[-1])

        self.parsed = directives

    def __index(self, directive):
        idx = self.index.get(directive.directive, [])
        idx.append(directive)
        self.index[directive.directive] = idx

    def __contains__(self, item):
        return item in self.index

    def __getattr__(self, name):
        if name in self.index:
            return self.get(name)
        else:
            raise AttributeError(
                '"{0s}" has not attribute "{1s}"'.format(
                    self.__class__.__name__,
                    name
                )
            )

    def get(self, directive):
        return self.index[directive] if directive in self.index else []

    def dict(self):
        dict_repr = {
            slot: getattr(self, slot)
            for slot in self.__slots__ if slot not in ('index', 'parsed')
        }

        dict_repr['parsed'] = [
            directive.dict() for directive in self.parsed
        ]
        return dict_repr


class CrossplaneConfig(object):
    __slots__ = ('index', 'files', 'configs')

    def __init__(self, configs=[]):
        self.index = {}
        self.files = []
        self.configs = configs

        self._setup_configs()

    def _setup_configs(self):
        configs = []
        for config_json in self.configs:
            configs.append(NGXConfigFile(**config_json))
            self.__index(configs[-1])

        self.configs = configs

    def __index(self, config):
        self.index[config.file] = config
        self.files.append(config.file)

    def __contains__(self, item):
        return item in self.index

    def __getattr__(self, name):
        if name in self.index:
            return self.get(name)
        else:
            raise AttributeError(
                '"{0s}" has not attribute "{1s}"'.format(
                    self.__class__.__name__,
                    name
                )
            )

    def get(self, file):
        return self.index[file] if file in self.index else None

    def get_include(self, idx):
        return self.index[self.files[idx]]

    def dict(self):
        return {
            'config': [config.dict() for config in self.configs]
        }


def xmap(payload):
    """
    Loads a crossplane.parse() payload into a CrossplaneConfig object and
    returns it.
    """
    return CrossplaneConfig(configs=payload['config'])


def ximport(filename, **kwargs):
    """
    Uses parser to parse an nginx config file and then creates native Python
    objects from the parsed structure.  These native objects can then be edited
    and output into a new crossplane structure.
    """
    payload = parse(filename, **kwargs)
    return xmap(payload)
