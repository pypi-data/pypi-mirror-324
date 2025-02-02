from __future__ import annotations

from typing import Literal, TypeAlias, overload

import msgspec
from architecture.utils.functions import run_sync
from intellibricks.llms import Synapse, SynapseCascade

from .contracts import Savable
from .types import PDFDocument, PPTXDocument

DocumentType: TypeAlias = Literal["pptx", "docx", "pdf", "xlsx"]


class DocumentCreator[T: Savable](msgspec.Struct, frozen=True):
    document_type: T
    """Type of the document beeing created"""

    @overload
    @classmethod
    def of(
        cls, document_type: Literal["pptx"], *, llm: Synapse | SynapseCascade
    ) -> DocumentCreator[PPTXDocument]: ...

    @overload
    @classmethod
    def of(
        cls, document_type: Literal["pdf"], *, llm: Synapse | SynapseCascade
    ) -> DocumentCreator[PDFDocument]: ...

    @classmethod
    def of(
        cls, document_type: DocumentType, *, llm: Synapse | SynapseCascade
    ) -> DocumentCreator[T]: ...

    def create(self, command: str) -> T:
        return run_sync(self.create_document_async, command=command)

    async def create_async(self, command: str) -> T: ...
