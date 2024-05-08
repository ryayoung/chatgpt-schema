from __future__ import annotations
from typing import Literal
from .config import Model


class UserMessage(Model):
    """
    A message at `Conversation.mapping[<id>].message` where author.role == 'user'
    """

    id: str
    author: Author
    create_time: float
    update_time: None
    content: TextContent | MultimodalTextContent
    status: Literal['finished_successfully']
    end_turn: None
    weight: float
    metadata: Metadata
    recipient: Literal['all']


class Author(Model):
    role: Literal['user']
    name: None
    metadata: Literal[{}]  # type:ignore


class TextContent(Model):
    content_type: Literal['text']
    parts: list[str]


class MultimodalTextContent(Model):
    content_type: Literal['multimodal_text']
    parts: list[str | ImageContentPart]


class ImageContentPart(Model):
    content_type: Literal['image_asset_pointer']
    asset_pointer: str
    size_bytes: int
    width: int
    height: int
    fovea: None
    metadata: None


class Metadata(Model):
    request_id: str | None = None
    timestamp_: Literal['absolute']
    message_type: None
    attachments: list[ImageAttachment | TextFileAttachment | URL] | None = None
    targeted_reply: str | None = None
    voice_mode_message: Literal[True] | None = None
    gizmo_id: str | None = None


class ImageAttachment(Model):
    name: str
    id: str
    size: int
    mimeType: str | None = None
    mime_type: str | None = None
    width: int | None = None
    height: int | None = None


class TextFileAttachment(Model):
    name: str
    id: str
    size: int
    mimeType: Literal['text/plain','application/pdf']
    fileTokenSize: int

class URL(Model):
    name: str
    url: str
    id: str
    size: int

# Keep at end of file
UserMessage.model_rebuild()
