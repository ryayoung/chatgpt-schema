from __future__ import annotations
from typing import Literal
from .config import Model


class SystemMessage(Model):
    """
    A message at `Conversation.mapping[<id>].message` where author.role == 'system'
    """

    id: str
    author: Author
    create_time: float | None
    update_time: None
    content: Content
    status: Literal['finished_successfully']
    end_turn: bool | None
    weight: float
    metadata: Metadata
    recipient: Literal['all']


class Author(Model):
    role: Literal['system']
    name: None
    metadata: Literal[{}]  # type:ignore


class Content(Model):
    content_type: Literal['text']
    parts: list[str]


class Metadata(Model):
    is_visually_hidden_from_conversation: Literal[True]
    is_complete: Literal[True] | None = None
    is_user_system_message: Literal[True] | None = None
    user_context_message_data: UserContextMessageData | None = None
    rebase_system_message: Literal[True] | None = None
    message_type: None = None
    model_slug: str | None = None
    default_model_slug: str | None = None
    parent_id: str | None = None
    request_id: str | None = None
    timestamp_: Literal['absolute'] | None = None
    attachments: list[Attachment] | None = None
    voice_mode_message: bool | None = None
    finish_details: FinishDetails | None = None
    gizmo_id: str | None = None


class FinishDetails(Model):
    type: Literal['stop']
    stop_tokens: list[float]

class Attachment(Model):
    id: str
    name: str
    mimeType: str


class UserContextMessageData(Model):
    about_user_message: str | None = None
    about_model_message: str | None = None


# Keep at end of file
SystemMessage.model_rebuild()
