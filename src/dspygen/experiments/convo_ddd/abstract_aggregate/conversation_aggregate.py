from munch import Munch

from dspygen.experiments.convo_ddd import (RecognizeIntentCommand,
                                              RecognizeEntityCommand,
                                                UpdateContextCommand,
                                                    TransitionStateCommand,
GenerateResponseCommand,
HandleUserQueryCommand,
                                           ContextUpdatedEvent,
                                           EntityRecognizedEvent,
                                           IntentRecognizedEvent,
                                           ResponseGeneratedEvent,
                                           StateTransitionEvent,
                                           UserInputReceivedEvent)

from dspygen.rdddy.abstract_aggregate import AbstractAggregate
from dspygen.modules.gen_pydantic_instance import instance
from dspygen.rdddy.actor_system import ActorSystem


class ConversationAggregate(AbstractAggregate):
    def __init__(self, conversation_id: str, actor_system: "ActorSystem"):
        super().__init__(actor_system)
        self.conversation_id = conversation_id
        self.context = Munch({"intent": None, "entity": None})
        self.state = "initial"

    async def handle_recognize_intent_command(self, command: RecognizeIntentCommand):
        # Simulate intent recognition logic
        intent = instance(IntentRecognizedEvent, command.user_input)  # Assume instance() magically does the job
        self.apply_event(intent)

    async def handle_recognize_entity_command(self, command: RecognizeEntityCommand):
        # Simulate entity recognition logic
        entity = instance(EntityRecognizedEvent, command.user_input)  # Assume instance() works similarly
        self.apply_event(entity)

    async def handle_update_context_command(self, command: UpdateContextCommand):
        if command.replace:
            self.context = command.updates
        else:
            self.context.update(command.updates)
        self.apply_event(ContextUpdatedEvent(content="Context updated"))

    async def handle_transition_state_command(self, command: TransitionStateCommand):
        self.state = command.new_state
        self.apply_event(StateTransitionEvent(content=f"Transitioned to {self.state} state"))

    async def handle_generate_response_command(self, command: GenerateResponseCommand):
        # Simplified response generation logic based on intent
        if self.context.get("intent") == "greeting":
            response = "Hello! How can I assist you today?"
        elif self.context.get("intent") == "inquiry":
            response = "What information are you seeking?"
        else:
            response = "I'm sorry, could you rephrase that?"

        self.apply_event(ResponseGeneratedEvent(content=response))

    async def handle_user_query_command(self, command: HandleUserQueryCommand):
        # Process user query and potentially invoke other commands based on the query
        self.apply_event(UserInputReceivedEvent(content=command.query))
        # Example: Recognize intent from the user query
        await self.handle_recognize_intent_command(RecognizeIntentCommand(user_input=command.query))
        # Generate a response based on recognized intent
        await self.handle_generate_response_command(GenerateResponseCommand(intent=self.context.get("intent", "")))

    def apply_event(self, event):
        if isinstance(event, IntentRecognizedEvent):
            self.context['intent'] = event.intent_name
        elif isinstance(event, EntityRecognizedEvent):
            self.context['entity'] = event.entity_name
        # Include handling for other event types as needed
        else:
            # It's helpful to log or handle the case where an event is not recognized
            print(f"Unhandled event type: {type(event)}")
