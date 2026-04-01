# -*- coding: utf-8 -*-
import typing as t


class NgxParserBaseException(Exception):
    def __init__(self, strerror: str, filename: t.Optional[str], lineno: t.Optional[int]) -> None:
        self.args = (strerror, filename, lineno)
        self.filename = filename
        self.lineno = lineno
        self.strerror = strerror

    def __str__(self) -> str:
        if self.lineno is not None:
            return '%s in %s:%s' % self.args
        else:
            return '%s in %s' % self.args


class NgxParserSyntaxError(NgxParserBaseException):
    pass


class NgxParserDirectiveError(NgxParserBaseException):
    pass


class NgxParserDirectiveArgumentsError(NgxParserDirectiveError):
    pass


class NgxParserDirectiveContextError(NgxParserDirectiveError):
    pass


class NgxParserDirectiveUnknownError(NgxParserDirectiveError):
    pass
