# -*- coding: utf-8 -*-
from crossplane.analyzer import register_external_directives
from crossplane.builder import register_external_builder
from crossplane.ext.abstract import CrossplaneExtension


class LuaPlugin(CrossplaneExtension):
    directives = {
        'init_by_lua': [],
        'init_worker_by_lua': [],
        'set_by_lua': [],
        'rewrite_by_lua': [],
        'access_by_lua': [],
        'content_by_lua': [],
        'header_filter_by_lua': [],
        'body_filter_by_lua': [],
        'log_by_lua': [],
    }

    def register_extension(self):
        register_external_builder(directives=self.directives, builder=self.build)

    def lex(self, token_iterator, directive):
        raise NotImplementedError

    def parse(self, stmt, parsing, tokens, ctx=(), consume=False):
        raise NotImplementedError

    def build(self, stmt, padding, state, indent=4, tabs=False):
        built = stmt['directive']
        if built == 'set_by_lua':
            block = stmt['args'][1]
            built += " %s" % stmt['args'][0]
        else:
            block = stmt['args'][0]
        return built + " '" + block + "';"
