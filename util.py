from dataclasses import dataclass
from typing import List, Dict, Any
from pprint import pprint
import tiktoken
from model.conversation import Conversation, RootNode, MessageNode
from model.user import MultimodalTextContent
from model.assistant import CodeContent
from model.tool import BrowserDisplayContent, ErrorContent, ExecutionOutputContent, BrowserQuoteContent, ImageContentPart, ToolMultimodalTextContent

@dataclass
class Message:
    role: str
    content: List[str]

    @classmethod
    def from_mapping(cls, mapping: Dict[str, Any]) -> 'Message':
        role = mapping.get('message', {}).get('author', {}).get('role', None)
        content = mapping.get('message', {}).get('content', {}).get('parts', [''])
        return cls(role, content)
    
@dataclass
class ConversationHistory:
    title: str
    id_: str
    messages: List[Message]

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'ConversationHistory':
        title = data['title']
        id_ = data['id']
        messages = [Message.from_mapping(value) for key, value in data['mapping'].items() if value.get('message')]
        return cls(title, id_, messages)
    
    def add_message(self, message: Message):
        self.messages.append(message)

def message_to_string(node: MessageNode) -> str:
    """
    Handle different message types and return the message content as a string. Note that this function doesn't handle the case where the message is a image content. Usually, the content is stored in node.message.content.parts in a list[str] format, so we only need to handle when it's not the case.
    Args:
        node (MessageNode): the node to extract the message content from
    Returns: 
        str: the message content as a string
    """
    # handle for assitant message
    if isinstance(node.message.content, CodeContent):
        text = node.message.content.text
    # handle for user message
    elif isinstance(node.message.content, MultimodalTextContent) | isinstance(node.message.content, ToolMultimodalTextContent):
        text_parts = []
        for part in node.message.content.parts:
            if isinstance(part, str):
                text_parts.append(part)
        text = " ".join(text_parts)
    # handle for tool message
    elif isinstance(node.message.content, BrowserDisplayContent):
        text = node.message.content.result
    elif isinstance(node.message.content,  ExecutionOutputContent) | isinstance(node.message.content, ErrorContent) | isinstance(node.message.content, BrowserQuoteContent):
        text = node.message.content.text
    # since image content doesn't have text info and it's uncertain how the token is calculated for images, we return an empty string
    elif isinstance(node.message.content, ImageContentPart):
        text = ""
    else:
        text = " ".join(node.message.content.parts)
    return text

def sub_converstaions(conversation: Conversation) -> list:
    """
    Extract the sub-conversations from the conversation tree. The token consumption is calculated based on the sub-conversations. From the root node, traverse the tree using depth-first search and construct all sub-conversations from root to leaf nodes.
    Args:
        node (Conversation): the root node of the conversation tree
    Returns:
        list: a list of sub-conversations
    """

    def dfs(conversation, node_id, current_path, results):
        current_node = conversation.mapping[node_id]
        
        # Append the current node's message to the path
        current_path.append(current_node)

        # If the current node is a leaf node, append the current_path to results
        if not current_node.children:
            results.append(current_path.copy())
        else:
            # Recurse for each child
            for child in current_node.children:
                dfs(conversation, child, current_path, results)
        
        # Remove the last node from current_path to backtrack as we return from recursion
        current_path.pop()

    results = []
    for node in conversation.mapping.values():
        # Start DFS from the root node
        if isinstance(node, RootNode):
            for child in node.children:
                dfs(conversation, child, [], results)
    return results


def token_consumption_per_chat(conversation: list, model: str) -> list:
    # model args: gpt-4, gpt-3.5-turbo, text-embedding-ada-002, text-embedding-3-small, text-embedding-3-large
    encoding = tiktoken.encoding_for_model(model)
    input_tokens = 0
    output_tokens = 0
    total_net_tokens = 0
    total_tokens = 0
    for message in conversation:
        text = message_to_string(message)
        role = message.message.author.role
        num_tokens = len(encoding.encode(text))
        total_net_tokens += num_tokens
        if role != "user" and role != "tool":
            output_tokens += num_tokens
        else:
            input_tokens += total_net_tokens
    total_tokens = input_tokens + output_tokens
    return [input_tokens, output_tokens, total_tokens]


def pricing_calculation(input_tokens: float, output_tokens: float, model: str) -> float:
    if model == "gpt-4":
        token_consumption = input_tokens/1000 * 0.03 + output_tokens/1000 * 0.06
    elif model == "gpt-3.5-turbo":
        token_consumption = input_tokens/1000 * 0.0005 + output_tokens/1000 * 0.0015
    return token_consumption