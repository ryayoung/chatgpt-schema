from __future__ import annotations
from typing import Literal
from pydantic import Field
from .config import Model, DefaultToolName, PluginName


class ToolMessage(Model):
    """
    A message at `Conversation.mapping[<id>].message` where author.role == 'tool'
    """

    id: str
    author: Author
    create_time: float
    update_time: float | None
    content: Content
    status: Literal['finished_successfully', 'in_progress']
    end_turn: None
    weight: float
    metadata: Metadata
    recipient: Literal['all']


class Author(Model):
    role: Literal['tool']
    name: DefaultToolName | PluginName
    metadata: Literal[{}]  # type:ignore


class TextContent(Model):
    content_type: Literal['text']
    parts: list[str]


class ErrorContent(Model):
    content_type: Literal['system_error']
    name: str
    text: str


class ExecutionOutputContent(Model):
    content_type: Literal['execution_output']
    text: str


class BrowserDisplayContent(Model):
    content_type: Literal['tether_browsing_display']
    result: str
    summary: str | None
    assets: Literal[[], None]  # type:ignore


class BrowserQuoteContent(Model):
    content_type: Literal['tether_quote']
    url: str
    domain: str
    text: str
    title: str


class MultimodalTextContent(Model):
    content_type: Literal['multimodal_text']
    parts: list[ImageContentPart]


class ImageContentPart(Model):
    content_type: Literal['image_asset_pointer']
    asset_pointer: str
    size_bytes: int
    width: int
    height: int
    fovea: int
    metadata: dict


Content = (
    TextContent
    | ErrorContent
    | ExecutionOutputContent
    | BrowserDisplayContent
    | BrowserQuoteContent
    | MultimodalTextContent
)


class Metadata(Model):
    message_type: None
    model_slug: str
    timestamp_: Literal['absolute']
    default_model_slug: str | None = None
    parent_id: str | None = None
    request_id: str | None = None
    is_complete: bool | None = None
    aggregate_result: dict | None = None
    cite_metadata: dict | None = Field(alias='_cite_metadata', default=None)
    command: BrowserCommand | None = None
    args: list[str] | list[int] | list[list[int]] | None = None
    status: Literal['finished', 'failed'] | None = None
    invoked_plugin: InvokedPlugin | None = None
    finish_details: FinishDetails | None = None


BrowserCommand = Literal[
    'search',
    'mclick',
    'click',
    'quote_lines',
    'back',
    'quote',
    'open_url',
    'scroll',
]


class FinishDetailsInterrupted(Model):
    type: Literal['interrupted']


FinishDetails = FinishDetailsInterrupted


class InvokedPlugin(Model):
    type: Literal['remote']
    namespace: str
    plugin_id: str
    http_response_status: int


# Keep at end of file
ToolMessage.model_rebuild()
