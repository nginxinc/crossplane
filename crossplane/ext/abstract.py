# -*- coding: utf-8 -*-
import typing as t
from crossplane.analyzer import register_external_directives
from crossplane.lexer import register_external_lexer
from crossplane.parser import register_external_parser
from crossplane.builder import register_external_builder
from crossplane.typedefs import StatusType, DictResponse, DictFile, DictStatement


class CrossplaneExtension(object):
    directives: t.Dict[str, t.Any] = {}

    def register_extension(self) -> None:
        register_external_directives(directives=self.directives)
        register_external_lexer(directives=self.directives, lexer=self.lex)
        register_external_parser(directives=self.directives, parser=self.parse)
        register_external_builder(directives=self.directives, builder=self.build)

    def lex(self, token_iterator: t.Iterator[t.Tuple[str, int]], directive: str) -> t.Iterable[t.Tuple[str, int, bool]]:
        raise NotImplementedError

    def parse(self, stmt: DictStatement, parsing: None, tokens: t.List[str], ctx: t.Tuple[str, ...] = (), consume: bool=False) -> None:
        raise NotImplementedError

    def build(self, stmt: DictStatement, padding: str, indent: int=4, tabs: bool=False) -> str:
        raise NotImplementedError
