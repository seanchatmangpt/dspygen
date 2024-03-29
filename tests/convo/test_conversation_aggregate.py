import pytest
import asyncio
from unittest.mock import patch

from dspygen.experiments.convo_ddd.abstract_aggregate.conversation_aggregate import ConversationAggregate
from dspygen.experiments.convo_ddd.abstract_command.generate_response_command import GenerateResponseCommand
from dspygen.experiments.convo_ddd.abstract_command.handle_user_query_command import HandleUserQueryCommand
from dspygen.experiments.convo_ddd.abstract_command.recognize_entity_command import RecognizeEntityCommand
from dspygen.experiments.convo_ddd.abstract_command.recognize_intent_command import RecognizeIntentCommand
from dspygen.experiments.convo_ddd.abstract_command.transition_state_command import TransitionStateCommand
from dspygen.experiments.convo_ddd.abstract_command.update_context_command import UpdateContextCommand
from dspygen.experiments.convo_ddd.abstract_event.context_updated_event import ContextUpdatedEvent
from dspygen.experiments.convo_ddd.abstract_event.entity_recognized_event import EntityRecognizedEvent
from dspygen.experiments.convo_ddd.abstract_event.intent_recognized_event import IntentRecognizedEvent
from dspygen.experiments.convo_ddd.abstract_event.response_generated_event import ResponseGeneratedEvent
from dspygen.experiments.convo_ddd.abstract_event.state_transition_event import StateTransitionEvent
from dspygen.experiments.convo_ddd.abstract_event.user_input_received_event import UserInputReceivedEvent
from dspygen.rdddy.actor_system import ActorSystem

@pytest.fixture()
def mock_instance(monkeypatch):
    def mock_return(model, user_input):
        if model == IntentRecognizedEvent:
            return IntentRecognizedEvent(intent_name="query_intent")
        elif model == RecognizeEntityCommand:
            return EntityRecognizedEvent(entity_name="query_entity")
        elif model == GenerateResponseCommand:
            return ResponseGeneratedEvent(content="This is a response.")
        else:
            return None
    monkeypatch.setattr("dspygen.experiments.convo_ddd.abstract_aggregate.conversation_aggregate.instance", mock_return)

# @pytest.mark.asyncio
# async def test_conversation_flow(mock_instance):
#     """
#     Test the ConversationAggregate's capability to process a user query through its lifecycle:
#     recognizing intent and entity, updating context, transitioning state, and generating a response.
#
#     The test uses mocked instances for intent and entity recognition to simulate the conversation flow.
#     """
#     actor_system = ActorSystem()
#     conversation_aggregate = ConversationAggregate(actor_system=actor_system)
#
#     # Process user query command
#     user_query_command = HandleUserQueryCommand(query="How's the weather?")
#     await conversation_aggregate.handle_user_query_command(user_query_command)
#
#     await asyncio.sleep(0)  # Allow time for message processing
#
#     # Assertions are based on the side effects observed through the aggregate's state changes
#     assert conversation_aggregate.context['intent'] == "query_intent"
#     # assert conversation_aggregate.context['entity'] == "query_entity"
#     # Assuming the state transition and response generation would also update the context or state accordingly
#     # These are simplistic checks; a real implementation might involve more detailed state or context assertions
#
#     # This simplified test assumes direct effects and does not capture event broadcasting or actor communication
