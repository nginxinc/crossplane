# -*- coding: utf-8 -*-
import hashlib

from .parser import parse

import sys
PYTHON3 = True if sys.version_info[0] >= 3 else False


def _init_directive(parent, directive_json):
    if 'block' in directive_json:
        return NginxBlockDirective(parent=parent, **directive_json)
    else:
        return NginxDirective(parent=parent, **directive_json)


class CrossplaneObject(object):
    __slots__ = tuple()
    __meta_slots__ = tuple()

    def __hash__(self):
        return hash(self.hexdigest())

    def __eq__(self, other):
        if callable(getattr(other, '__hash__', None)):
            return hash(self) == hash(other)
        else:
            return False

    def __contains__(self, item):
        """
        Single directives don't really have a contains operator, so this method
        is included as a stub to allow for recursive logic to be conveniently
        inheritied.
        """
        return False

    def get(self, directive):
        """
        Like __contains__, this is stubbed for convenient recursion.
        """
        return []

    def to_crossplane(self, include_meta=True):
        result = {}

        # exclude slots unique to object layer
        for slot in self.__slots__:
            if slot not in self.__meta_slots__:
                result[slot] = getattr(self, slot)

        return result

    def hexdigest(self):
        crossplane_dict = self.to_crossplane(include_meta=False)

        if PYTHON3:
            return hashlib.sha256(
                str(crossplane_dict).encode('utf-8')
            ).hexdigest()
        else:
            return hashlib.sha256(
                unicode(crossplane_dict).encode('utf-8')
            ).hexdigest()


class NginxDirective(CrossplaneObject):
    __slots__ = ('parent', 'directive', 'line', 'args', 'includes')
    __meta_slots__ = ('parent',)

    def __init__(self, directive, args, line=None, includes=None, parent=None):
        self.parent = parent
        self.directive = directive
        self.line = line
        self.args = args
        self.includes = includes if includes is not None else []

    def to_crossplane(self, include_meta=True):
        result = super(NginxDirective, self).to_crossplane(include_meta=include_meta)

        # remove line if None
        if self.line is None or not include_meta:
            del result['line']

        # remove includes if not include directive
        if self.directive != 'include' or not include_meta:
            # since this can get called by super of NginxBlockDirective we need
            # to check that it is in the payload
            if 'includes' in result:
                del result['includes']

        return result

    def __setattr__(self, name, value):
        if PYTHON3:
            basestring = str
        else:
            basestring = (str, unicode)

        if name == 'args':
            if not isinstance(value, (list, tuple)) \
               and isinstance(value, basestring):
                value = value.split(' ')

        super(NginxDirective, self).__setattr__(name, value)

    @property
    def file(self):
        """
        Recursively walk the tree to find the containing file.
        """
        return self.parent.file

    def environment(self, *args):
        """
        Recursively scans parent blocks for a passed list of "context"
        diretives.  These are a list of directives which apply or may apply to
        this specific directive.  This method will return a dictionary of
        directives and their args which affect this directive.

        It follows NGINX inheritance which is, all-or-nothing, lowest level
        directive(s) apply.
        """
        environment = {}

        for directive_name in args:
            if directive_name in self:
                values = []

                # for each directive instance, get the args value and append to
                # currently tracked
                for directive in self.get(directive_name):
                    # rebuild multi arg directives
                    values.append(' '.join(directive.args))

                # add this context to context
                environment[directive_name] = \
                    environment.get(directive_name, []) + values

        # if there is a context in this directive/block then return it,
        # otherwise try to find one from the parent
        if len(environment) > 0:
            return environment, self
        elif self.parent is not None:
            return self.parent.environment(*args)
        else:
            return None, None


class NginxBlockDirective(NginxDirective):
    __slots__ = ('parent', 'index', 'directive', 'line', 'args', 'block')
    __meta_slots__ = ('parent', 'index')

    def __init__(self, directive, args, line=None, block=None, **kwargs):
        super(NginxBlockDirective, self).__init__(directive, args, line, **kwargs)
        self.index = {}
        self.block = block if block is not None else []

        self._setup_block()

    def _setup_block(self):
        directives = []
        for directive_json in self.block:
            directives.append(_init_directive(self, directive_json))
            self.__index(directives[-1])

        self.block = directives

    def __index(self, directive):
        idx = self.index.get(directive.directive, [])
        idx.append(directive)
        self.index[directive.directive] = idx

    def __contains__(self, item):
        return item in self.index

    def get(self, directive):
        return self.index[directive] if directive in self.index else []

    def to_crossplane(self, include_meta=True):
        result = super(NginxBlockDirective, self).to_crossplane(include_meta=include_meta)

        result['block'] = [
            directive.to_crossplane(include_meta=include_meta)
            for directive in self.block
        ]

        return result


class NginxConfigFile(CrossplaneObject):
    __slots__ = ('parent', 'index', 'file', 'parsed')
    __meta_slots__ = ('parent', 'index')

    def __init__(self, file='', parsed=None, parent=None, **kwargs):
        self.parent = parent

        self.index = {}
        self.file = file
        self.parsed = parsed if parsed is not None else []

        self._setup_parsed()

    def _setup_parsed(self):
        directives = []
        for directive_json in self.parsed:
            directives.append(_init_directive(self, directive_json))
            self.__index(directives[-1])

        self.parsed = directives

    def __index(self, directive):
        idx = self.index.get(directive.directive, [])
        idx.append(directive)
        self.index[directive.directive] = idx

    def __contains__(self, item):
        return item in self.index

    def get(self, directive):
        return self.index[directive] if directive in self.index else []

    def to_crossplane(self, include_meta=True):
        result = super(NginxConfigFile, self).to_crossplane(include_meta=include_meta)

        result['parsed'] = [
            directive.to_crossplane(include_meta=include_meta)
            for directive in self.parsed
        ]

        return result


class CrossplaneConfig(CrossplaneObject):
    __slots__ = ('index', 'files', 'configs')
    __meta_slots__ = ('index', 'files')

    def __init__(self, configs=None):
        self.index = {}
        self.files = []
        self.configs = configs if configs is not None else []

        self._setup_configs()

    def _setup_configs(self):
        configs = []
        for config_json in self.configs:
            configs.append(NginxConfigFile(parent=self, **config_json))
            self.__index(configs[-1])

        self.configs = configs

    def __index(self, config):
        self.index[config.file] = config
        self.files.append(config.file)

    def __contains__(self, item):
        return item in self.index

    def get(self, file):
        return self.index[file] if file in self.index else None

    def get_include_idx(self, idx):
        return self.index[self.files[idx]]

    def to_crossplane(self, include_meta=True):
        result = {}

        result['config'] = [
            config.to_crossplane(include_meta=include_meta)
            for config in self.configs
        ]

        return result


def map(payload):
    """
    Loads a crossplane.parse() payload into a CrossplaneConfig object and
    returns it.
    """
    return CrossplaneConfig(configs=payload['config'])


def load(filename, **kwargs):
    """
    Uses parser to parse an nginx config file and then creates native Python
    objects from the parsed structure.  These native objects can then be edited
    and output into a new crossplane structure.
    """
    payload = parse(filename, **kwargs)
    return map(payload)
