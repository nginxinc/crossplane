# -*- coding: utf-8 -*-

import abc
from crossplane import analyzer, lexer, parser, builder
from crossplane.objects import NginxDirective, NginxBlockDirective


class CrossplaneExtension(object):
    directives = {}

    def register_extension(self):
        for directive, bitmasks in self.directives.iteritems():
            analyzer.register_external_directive(directive=directive, bitmasks=bitmasks)
        lexer.register_external_lexer(directives=self.directives.keys(), lexer=self.lex)
        parser.register_external_parser(directives=self.directives.keys(), parser=self.parse)
        builder.register_external_builder(directives=self.directives.keys(), builder=self.build)

    def lex(self, token_iterator, directive):
        raise NotImplementedError

    def parse(self, stmt, parsing, tokens, ctx=(), consume=False):
        raise NotImplementedError

    def build(self, stmt, padding, state, indent=4, tabs=False):
        raise NotImplementedError


class ExternalDirective(NginxDirective):
    pass


class ExternalBlockDirective(NginxBlockDirective):
    pass
