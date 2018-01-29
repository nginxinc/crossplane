# -*- coding: utf-8 -*-
from .parser import parse


#
# Functions
#

def _init_directive(parent, directive_json):
    if 'block' in directive_json:
        return NGXBlockDirective(parent=parent, **directive_json)
    else:
        return NGXDirective(parent=parent, **directive_json)


#
# Classes
#

class NGXDirective(object):
    __slots__ = ('parent', 'directive', 'line', 'args', 'includes')

    def __init__(self, directive='', line=0, args=[], includes=[], parent=None,
                 **kwargs):
        self.parent = parent

        self.directive = directive
        self.line = line
        self.args = args
        self.includes = []

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

    def dict(self):
        result = {}

        for slot in self.__slots__:
            if slot not in ('parent',):
                result[slot] = getattr(self, slot)

        return result

    @property
    def file(self):
        """
        Recursively walk the tree to find the containing file.
        """
        return self.parent.file

    @property
    def location(self):
        """
        Return filename, line number of current directive.
        """
        return self.file, self.line

    def context(self, *args):
        """
        Recursively scans parent blocks for a passed list of "context"
        diretives.  These are a list of directives which apply or may apply to
        this specific directive.  This method will return a dictionary of
        directives and their args which affect this directive.

        It follows NGINX inheritance which is, all-or-nothing, lowest level
        directive(s) apply.
        """
        context = {}

        for directive_name in args:
            if directive_name in self:
                values = []

                # for each directive instance, get the args value and append to
                # currently tracked
                for directive in self.get(directive_name):
                    # rebuild multi arg directives
                    values.append(' '.join(directive.args))

                # add this context to context
                context[directive_name] = \
                    context.get(directive_name, []) + values

        # if there is a context in this directive/block then return it,
        # otherwise try to find one from the parent
        if len(context) > 0:
            return context, self
        elif self.parent is not None:
            return self.parent.context(*args)
        else:
            return None, None


class NGXBlockDirective(NGXDirective):
    __slots__ = ('parent', 'index', 'directive', 'line', 'args', 'block')

    def __init__(self, block=[], **kwargs):
        super(NGXBlockDirective, self).__init__(**kwargs)
        self.index = {}
        self.block = block

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

    def dict(self):
        result = {}

        for slot in self.__slots__:
            if slot not in ('parent', 'index', 'block'):
                result[slot] = getattr(self, slot)

        result['block'] = [
            directive.dict() for directive in self.block
        ]

        return result


class NGXConfigFile(object):
    __slots__ = ('parent', 'index', 'file', 'parsed')

    def __init__(self, file='', parsed=[], parent=None, **kwargs):
        self.parent = parent

        self.index = {}
        self.file = file
        self.parsed = parsed

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

    def dict(self):
        result = {}

        for slot in self.__slots__:
            if slot not in ('parent', 'index', 'parsed'):
                result[slot] = getattr(self, slot)

        result['parsed'] = [
            directive.dict() for directive in self.parsed
        ]

        return result


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
            configs.append(NGXConfigFile(parent=self, **config_json))
            self.__index(configs[-1])

        self.configs = configs

    def __index(self, config):
        self.index[config.file] = config
        self.files.append(config.file)

    def __contains__(self, item):
        return item in self.index

    def get(self, file):
        return self.index[file] if file in self.index else None

    def get_include(self, idx):
        return self.index[self.files[idx]]

    def dict(self):
        result = {}

        result['config'] = [
            config.dict() for config in self.configs
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
