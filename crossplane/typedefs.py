# -*- coding: utf-8 -*-
import typing as t

# This construction only required unless crossplane supports python<3.10 (for TypeAlias) or at least python<3.8 (for TypedDict and Literal)
if t.TYPE_CHECKING:
    from typing_extensions import TypeAlias, TypedDict, Literal
    StatusType: TypeAlias = Literal['ok', 'failed']

    class DictStatementBase(TypedDict):
        directive: str
        line: int
        args: t.List[str]

    class DictStatement(DictStatementBase, total=False):
        includes: t.List[int]
        block: t.List['DictStatement']
        comment: str
        file: str

    class DictFileError(TypedDict):
        error: str
        line: t.Optional[int]

    class DictFile(TypedDict):
        file: str
        status: StatusType
        errors: t.List[DictFileError]
        parsed: t.List[DictStatement]

    class DictErrorBase(TypedDict):
        error: str
        file: str
        line: t.Optional[int]

    class DictError(DictErrorBase, total=False):
        callback: t.Any

    class DictResponse(TypedDict):
        status: StatusType
        errors: t.List[DictError]
        config: t.List[DictFile]
else:
  StatusType = str
  DictResponse = DictError = DictFile = DictFileError = DictStatement = dict

__all__ = ['StatusType', 'DictResponse', 'DictError', 'DictFile', 'DictFileError', 'DictStatement']
