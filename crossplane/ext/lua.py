# -*- coding: utf-8 -*-

from .abstract import ExternalDirective
from crossplane import lexer, builder, objects
from crossplane.errors import NgxParserBaseException
from crossplane.ext.abstract import CrossplaneExtension


class LuaBlockPlugin(CrossplaneExtension):
    """
    This plugin adds special handling for Lua code block directives (*_by_lua_block)
    We don't need to handle non-block or file directives because those are parsed
    correctly by base Crossplane functionality.
    """

    def __init__(self):
        super(LuaBlockPlugin, self).__init__()

        # todo maybe: populate the actual directive bit masks if analyzer/parser logic is needed
        self.directives = {
            'access_by_lua_block' : [],
            'balancer_by_lua_block' : [],
            'body_filter_by_lua_block' : [],
            'content_by_lua_block' : [],
            'header_filter_by_lua_block' : [],
            'init_by_lua_block' : [],
            'init_worker_by_lua_block' : [],
            'log_by_lua_block' : [],
            'rewrite_by_lua_block' : [],
            'set_by_lua_block' : [],
            'ssl_certificate_by_lua_block' : [],
            'ssl_session_fetch_by_lua_block' : [],
            'ssl_session_store_by_lua_block' : [],
        }

    def register_extension(self):
        lexer.register_external_lexer(lexer=self.lex, directives=self.directives.keys())
        builder.register_external_builder(builder=self.build, directives=self.directives.keys())
        objects.register_external_object(object_class=LuaBlockDirective, directives=self.directives.keys())

    def lex(self, token_iterator, directive):
        in_string = False
        string_enclose = None
        depth = 0
        token = ''

        # check that Lua block starts correctly
        while True:
            char, line = next(token_iterator)
            if not char.isspace():
                break

        if char != "{":
            reason = 'expected { to start Lua block'
            raise LuaBlockParserSyntaxError(reason, filename=None, lineno=line)
        depth += 1

        # Grab everything in Lua block as a single token
        # and watch for curly brace '{' in strings
        for char, line in token_iterator:
            if char == '{' and not in_string:
                depth += 1
            elif char == '}' and not in_string:
                depth -= 1
            elif char == '"' or char == '\'':
                if in_string and string_enclose == char:
                    in_string = False
                    string_enclose = None
                elif not in_string:
                    in_string = True
                    string_enclose = char

            if depth < 0:
                reason = 'unxpected "}"'
                raise LuaBlockParserSyntaxError(reason, filename=None, lineno=line)

            if depth == 0:
                yield (token, line)
                yield (u";", line)
                raise StopIteration
            token += char

    def lex_set_by_lua_block(self, token_iterator):
        """
        https://github.com/openresty/lua-nginx-module#set_by_lua_block
        The sole *_by_lua_block directive that has an arg
        :param token_iterator:
        :return:
        """
        pass

    def parse(self, parsing, tokens, ctx=(), consume=False):
        pass

    def build(self, stmt, padding, state, indent=4, tabs=False):
        return stmt['directive'] + ' {' + stmt['args'][0] + '}'


class LuaBlockDirective(ExternalDirective):
    """
    For now we are treating everything inside of a Lua block
    as a single string argument, so there's no need to represent this
    as an extend of ExternalBlockDirective
    """
    pass


class LuaBlockParserSyntaxError(NgxParserBaseException):
    pass