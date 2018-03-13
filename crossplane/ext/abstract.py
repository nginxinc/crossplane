# -*- coding: utf-8 -*-

import abc
from crossplane import analyzer, lexer, parser, builder
from crossplane.objects import NginxDirective, NginxBlockDirective


class CrossplaneExtension(object):

    @abc.abstractproperty
    def directives(self):
        pass

    def register_extension(self):
        for directive, bitmasks in self.directives.iteritems():
            analyzer.register_external_directive(directive=directive, bitmasks=bitmasks)
        lexer.register_external_lexer(directives=self.directives.keys(), lexer=self.lex)
        parser.register_external_parser(directives=self.directives.keys(), parser=self.parse)
        builder.register_external_builder(directives=self.directives.keys(), builder=self.build)

    @abc.abstractmethod
    def lex(self, token_iterator, directive):
        pass

    @abc.abstractmethod
    def parse(self, statement, parsing, tokens, ctx=(), consume=False):
        pass

    @abc.abstractmethod
    def build(self, stmt, padding, state, indent=4, tabs=False):
        pass


class ExternalDirective(NginxDirective):
    pass


class ExternalBlockDirective(NginxBlockDirective):
    pass
