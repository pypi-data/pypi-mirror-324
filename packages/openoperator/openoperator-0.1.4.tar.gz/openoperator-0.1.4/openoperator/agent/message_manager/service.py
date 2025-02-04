from __future__ import annotations

import json
import logging
import re
from datetime import datetime
from typing import List, Optional, Type

from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)

from openoperator.agent.message_manager.views import MessageHistory, MessageMetadata
from openoperator.agent.prompts import AgentMessagePrompt, SystemPrompt, TaskPrompt
from openoperator.agent.task_manager.service import Task
from openoperator.agent.views import ActionResult, AgentOutput
from openoperator.browser.views import BrowserState

logger = logging.getLogger(__name__)


class MessageManager:
    def __init__(
        self,
        action_descriptions: str,
        system_prompt_class: Type[SystemPrompt],
        max_input_tokens: int = 128000,
        estimated_characters_per_token: int = 3,
        image_tokens: int = 800,
        include_attributes: List[str] = [],
        max_error_length: int = 400,
        max_actions_per_step: int = 10,
        initial_context: Optional[str] = None,
    ):
        self.system_prompt_class = system_prompt_class
        self.max_input_tokens = max_input_tokens
        self.history = MessageHistory()
        self.action_descriptions = action_descriptions
        self.estimated_characters_per_token = estimated_characters_per_token
        self.image_tokens = image_tokens
        self.include_attributes = include_attributes
        self.max_error_length = max_error_length
        self.initial_context = initial_context
        self.max_actions_per_step = max_actions_per_step

        self.tool_id = 1
        self._initialize_conversation()

    def _task_instructions(self, task: Task) -> HumanMessage:
        task_prompt = TaskPrompt(task)
        return task_prompt.get_user_message()

    def _initialize_conversation(self) -> None:
        """Sets up the conversation history as used in both __init__ and reset_messages."""
        # Start fresh
        self.history = MessageHistory()

        # Build the system prompt
        system_message = self.system_prompt_class(
            self.action_descriptions,
            current_date=datetime.now(),
            max_actions_per_step=self.max_actions_per_step,
        ).get_system_message()
        self._add_message_with_tokens(system_message)
        self.system_prompt = system_message

        # Optional context
        if self.initial_context:
            context_message = HumanMessage(content=self.initial_context)
            self._add_message_with_tokens(context_message)

        # Initial tool call (example)
        tool_calls = [
            {
                'name': 'AgentOutput',
                'args': {
                    'current_state': {
                        'evaluation_previous_goal': 'Unknown - No previous actions to evaluate.',
                        'memory': '',
                        'next_goal': 'Start browser',
                    },
                    'action': [],
                },
                'id': str(self.tool_id),
                'type': 'tool_call',
            }
        ]
        example_tool_call = AIMessage(content='', tool_calls=tool_calls)
        self._add_message_with_tokens(example_tool_call)

        # Corresponding ToolMessage
        tool_message = ToolMessage(
            content='Browser started',
            tool_call_id=str(self.tool_id),
        )
        self._add_message_with_tokens(tool_message)
        self.tool_id += 1

    def reset_messages(self) -> None:
        """
        Clears the message history and re-initializes the conversation
        as it was in the constructor (system prompt, optional context,
        and the initial example tool call).
        """
        self._initialize_conversation()

    def set_task(self, task: Task) -> None:
        """
        Set a new task and add the corresponding task instructions to the message history.
        If a task was previously set, you may want to handle it accordingly (e.g., by resetting the history).
        """
        task_message = self._task_instructions(task)
        self._add_message_with_tokens(task_message)

    def _add_message_with_tokens(self, message: BaseMessage) -> None:
        """Add message with token count metadata."""
        token_count = self._count_tokens(message)
        metadata = MessageMetadata(input_tokens=token_count)
        self.history.add_message(message, metadata)

    def _count_tokens(self, message: BaseMessage) -> int:
        """Count tokens in a message using the model's tokenizer (approximate if none)."""
        tokens = 0
        if isinstance(message.content, list):
            for item in message.content:
                if 'image_url' in item:
                    tokens += self.image_tokens
                elif isinstance(item, dict) and 'text' in item:
                    tokens += self._count_text_tokens(item['text'])
        else:
            msg = message.content
            # If there's a tool_calls attribute, include it in token approximation
            if hasattr(message, 'tool_calls'):
                msg += str(message.tool_calls)  # type: ignore
            tokens += self._count_text_tokens(msg)
        return tokens

    def _count_text_tokens(self, text: str) -> int:
        return len(text) // self.estimated_characters_per_token

    def add_state_message(
        self,
        state: BrowserState,
        result: Optional[List[ActionResult]] = None,
        use_vision: bool = False,
    ) -> None:
        """Add browser state as human message."""
        if result:
            for r in result:
                if r.include_in_memory:
                    if r.extracted_content:
                        msg = HumanMessage(content='Action result: ' + str(r.extracted_content))
                        self._add_message_with_tokens(msg)
                    if r.error:
                        msg = HumanMessage(content='Action error: ' + str(r.error)[-self.max_error_length :])
                        self._add_message_with_tokens(msg)
                    # Once added to history, don't add again
                    result = None

        state_message = AgentMessagePrompt(
            state,
            result,
            use_vision=use_vision,
            include_attributes=self.include_attributes,
            max_error_length=self.max_error_length,
        ).get_user_message()
        self._add_message_with_tokens(state_message)

    def _remove_last_state_message(self) -> None:
        """Remove last state message from history."""
        if len(self.history.messages) > 2 and isinstance(self.history.messages[-1].message, HumanMessage):
            self.history.remove_message()

    def add_model_output(self, model_output: AgentOutput) -> None:
        """Add model output as AI message."""
        tool_calls = [
            {
                'name': 'AgentOutput',
                'args': model_output.model_dump(mode='json', exclude_unset=True),
                'id': str(self.tool_id),
                'type': 'tool_call',
            }
        ]
        msg = AIMessage(content='', tool_calls=tool_calls)
        self._add_message_with_tokens(msg)

        # Add an empty ToolMessage for the step
        tool_message = ToolMessage(
            content='',
            tool_call_id=str(self.tool_id),
        )
        self._add_message_with_tokens(tool_message)
        self.tool_id += 1

    def get_messages(self) -> List[BaseMessage]:
        msg_list = [m.message for m in self.history.messages]
        total_input_tokens = 0
        logger.debug(f'Messages in history: {len(self.history.messages)}:')
        for m in self.history.messages:
            total_input_tokens += m.metadata.input_tokens
            logger.debug(f'{m.message.__class__.__name__} - Token count: {m.metadata.input_tokens}')
        logger.debug(f'Total input tokens: {total_input_tokens}')
        return msg_list

    def cut_messages(self):
        """Trim messages if total tokens exceed max_input_tokens."""
        diff = self.history.total_tokens - self.max_input_tokens
        if diff <= 0:
            return

        # Attempt to shorten the last message
        msg = self.history.messages[-1]

        # If last message has images, remove them first
        if isinstance(msg.message.content, list):
            text = ''
            for item in list(msg.message.content):
                if 'image_url' in item:
                    msg.message.content.remove(item)
                    diff -= self.image_tokens
                    msg.metadata.input_tokens -= self.image_tokens
                    self.history.total_tokens -= self.image_tokens
                    logger.debug(
                        f'Removed image with {self.image_tokens} tokens - total tokens now: '
                        f'{self.history.total_tokens}/{self.max_input_tokens}'
                    )
                elif 'text' in item and isinstance(item, dict):
                    text += item['text']
            msg.message.content = text
            self.history.messages[-1] = msg

        if diff <= 0:
            return

        proportion_to_remove = diff / msg.metadata.input_tokens
        if proportion_to_remove > 0.99:
            raise ValueError(
                f'Max token limit reached - history is too long. Reduce prompt size. '
                f'(Removing {proportion_to_remove*100:.1f}% of last message)'
            )
        logger.debug(f'Removing {proportion_to_remove * 100:.2f}% of the last message content')

        content = msg.message.content
        characters_to_remove = int(len(content) * proportion_to_remove)
        content = content[:-characters_to_remove]

        # Remove old message and add truncated one
        self.history.remove_message(-1)
        truncated_msg = HumanMessage(content=content)
        self._add_message_with_tokens(truncated_msg)
        last_msg = self.history.messages[-1]

        logger.debug(
            f'Truncated message token count: {last_msg.metadata.input_tokens}. '
            f'Total tokens: {self.history.total_tokens}/{self.max_input_tokens}.'
        )

    def convert_messages_for_non_function_calling_models(self, input_messages: List[BaseMessage]) -> List[BaseMessage]:
        """Convert messages for models that do not accept function/tool call format."""
        output_messages = []
        for message in input_messages:
            if isinstance(message, HumanMessage):
                output_messages.append(message)
            elif isinstance(message, SystemMessage):
                output_messages.append(message)
            elif isinstance(message, ToolMessage):
                output_messages.append(HumanMessage(content=message.content))
            elif isinstance(message, AIMessage):
                # If AIMessage has tool_calls, convert them to JSON text
                if message.tool_calls:
                    tool_calls_text = json.dumps(message.tool_calls)
                    output_messages.append(AIMessage(content=tool_calls_text))
                else:
                    output_messages.append(message)
            else:
                raise ValueError(f'Unknown message type: {type(message)}')
        return output_messages

    def merge_successive_human_messages(self, messages: List[BaseMessage]) -> List[BaseMessage]:
        """
        Some models disallow multiple consecutive human messages.
        Merge them into a single message if that happens.
        """
        merged_messages = []
        streak = 0
        for message in messages:
            if isinstance(message, HumanMessage):
                streak += 1
                if streak > 1:
                    if isinstance(message.content, list):
                        merged_messages[-1].content += message.content[0]['text']  # type: ignore
                    else:
                        merged_messages[-1].content += message.content
                else:
                    merged_messages.append(message)
            else:
                merged_messages.append(message)
                streak = 0
        return merged_messages

    def extract_json_from_model_output(self, content: str) -> dict:
        """Extract JSON from model output, handling code-block-wrapped JSON."""
        try:
            match = re.search(r'```(?:json)?\n(.*?)```', content, re.DOTALL)
            if match:
                content = match.group(1).strip()
            return json.loads(content)
        except json.JSONDecodeError as e:
            logger.warning(f'Failed to parse model output {content}: {str(e)}')
            raise ValueError('Could not parse response.')
