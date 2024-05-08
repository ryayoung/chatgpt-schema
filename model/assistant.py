"""
Defines the structure of an assistant message.
"""

from __future__ import annotations
from typing import Literal
from .config import Model, DefaultToolName, PluginName


class AssistantMessage(Model):
    """
    A message at `Conversation.mapping[<id>].message` where author.role == 'assistant'
    """

    id: str
    author: Author
    create_time: float
    update_time: None
    content: TextContent | CodeContent
    status: Status
    end_turn: bool | None
    weight: float
    metadata: Metadata
    recipient: Literal['all'] | DefaultToolName | PluginName


Status = Literal['finished_successfully', 'in_progress', 'finished_partial_completion']


class TextContent(Model):
    content_type: Literal['text']
    parts: list[str]


class CodeContent(Model):
    content_type: Literal['code']
    language: str
    text: str


class Author(Model):
    role: Literal['assistant']
    name: None
    metadata: Literal[{}]  # type:ignore


class Metadata(Model):
    finish_details: FinishDetails | None = None
    citations: CitationsList | None = None
    gizmo_id: None = None
    filter_out_for_training: Literal[True] | None = None
    is_complete: Literal[True] | None = None
    message_type: None
    model_slug: str
    default_model_slug: str | None = None
    pad: str | None = None
    parent_id: str | None = None
    request_id: str | None = None
    timestamp_: Literal['absolute']
    gizmo_id: str | None = None
    voice_mode_message: bool | None = None
    requested_model_slug: str | None = None

class FinishDetailsMaxTokens(Model):
    type: Literal['max_tokens']


class FinishDetailsStopTokens(Model):
    type: Literal['stop']
    stop_tokens: list[int]


class FinishDetailsStop(Model):
    type: Literal['stop']
    stop: str


class FinishDetailsInterrupted(Model):
    type: Literal['interrupted']


FinishDetails = (
    FinishDetailsStopTokens
    | FinishDetailsStop
    | FinishDetailsInterrupted
    | FinishDetailsMaxTokens
)


class InvalidCitation(Model):
    start_ix: int
    end_ix: int
    invalid_reason: str


class Citation(Model):
    start_ix: int
    end_ix: int
    citation_format_type: Literal['tether_og']
    metadata: CitationMetadata | None = None
    invalid_reason: str | None = None


class CitationMetadata(Model):
    type: Literal['webpage','file']
    name: str | None = None
    title: str | None = None
    id: str | None = None
    source: str | None = None
    url: str | None = None
    text: str
    pub_date: None = None
    extra: CitationMetadataExtra


class CitationMetadataExtra(Model):
    evidence_text: str | None = None
    # below works for my current conversation history but it's not sustainable
    # evidence_text: Literal['source', '(source)','(Reuters)','(Al Jazeera)', '(AP News)', '(ABC)', '(Wikipedia)'] | None = None
    cited_message_idx: int | None = None
    search_result_idx: int | None = None


class CitationLegacy(Model):
    start_ix: int
    end_ix: int
    metadata: CitationMetadataLegacy


class CitationMetadataLegacy(Model):
    title: str
    url: str
    text: str
    pub_date: None = None


CitationsList = list[Citation] | list[CitationLegacy] | list[InvalidCitation]


# Keep at end of file
AssistantMessage.model_rebuild()
