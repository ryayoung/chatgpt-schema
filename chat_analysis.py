import os
import pandas as pd
import json
from pprint import pprint
from util import Message, ConversationHistory, token_consumption_per_chat, pricing_calculation, sub_converstaions
from model.conversation import Conversation, RootNode, MessageNode
from model.tool import BrowserDisplayContent

with open('conversations.json') as f:
    data = json.load(f)

# create a list of conversation history from the raw data
convo_history = [Conversation(**obj) for obj in data]

# create a list of sub conversations from the conversation history
sub_convo = []
for convo in convo_history:
    sub_convo.extend(sub_converstaions(convo))

total_input_tokens = 0
total_output_tokens = 0
total_tokens = 0
num_messages = 0
for item in sub_convo:
    input_token, output_token, total_token = token_consumption_per_chat(item, 'gpt-4')
    total_input_tokens += input_token
    total_output_tokens += output_token
    total_tokens += total_token
    num_messages += len(item)
price = pricing_calculation(total_input_tokens, total_output_tokens, 'gpt-4')

# usage summary
print(f"Total number of conversations: {len(convo_history)}")
print(f"Total number of messages: {num_messages}")
print(f"Total input tokens: {total_input_tokens}")
print(f"Total output tokens: {total_output_tokens}")
print(f"Total tokens: {total_tokens}")
print(f"OpenAI API Pricing Equivalent: $ {round(price,2)}")