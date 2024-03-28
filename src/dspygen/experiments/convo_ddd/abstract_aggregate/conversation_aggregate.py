from typing import Optional

from munch import Munch
from pydantic import BaseModel, Field

import dspygen.experiments.convo_ddd as ddd

from dspygen.rdddy.abstract_aggregate import AbstractAggregate
from dspygen.modules.gen_pydantic_instance import instance
from dspygen.rdddy.actor_system import ActorSystem
from dspygen.utils.dspy_tools import init_dspy
from dspygen.utils.pydantic_tools import InstanceMixin

from pydantic import BaseModel, Field
from typing import Optional, List


class ContentModeration(BaseModel):
    """
    Defines the parameters and categories for moderating the content provided by users.
    It ensures that all user inputs are screened according to the specified moderation level
    and categories, if any, to maintain a safe and inclusive environment.

    Attributes:
        level (int): Specifies the general moderation level. It ranges from 1 (least restrictive)
                     to 5 (most restrictive), enabling precise control over content filtering
                     intensity. Setting this value is crucial for effective moderation.
        categories (Optional[List[str]]): Allows for the specification of particular content
                                          categories to moderate (e.g., ['violence', 'adult content']).
                                          This provides an additional layer of content filtering
                                          based on thematic concerns.
    """
    level: int = Field(..., ge=1, le=5,
                       description="Mandatory moderation intensity level, with 1 being the least restrictive and 5 the most.")
    categories: List[str] = Field(default=..., min_length=1,
                                  description="List of specific content categories to moderate. Leave as 'None' for general moderation based on level.")


class CharacterMessage(BaseModel, InstanceMixin):
    """
    Generates a creative and child-friendly message from a chosen character, ensuring the content is moderated
    according to the specified rules. This model is designed to engage users with entertaining and safe content
    from their favorite children's book characters, while actively preventing the generation of inappropriate responses.

    Attributes:
        user_input (str): The message or question from the user to which the character will respond.
                          This input is subject to moderation based on the specified settings to ensure
                          the content remains appropriate for all audiences.
        character (str): The name of the character responding to the user's input. This field can be
                         dynamically adjusted based on the theme of the input and moderation outcomes
                         to best fit the scenario.
        moderation (ContentModeration): Contains settings that define how the user input should be
                                        moderated. These settings ensure that the character's responses
                                        adhere to community guidelines and are appropriate for children.
        poem (str): The character's original, moderated poem created in response to the user's input.
                    This field must contain at least 50 characters, ensuring a thoughtful and engaging
                    response that has passed through the moderation process.
    """
    user_input: str = Field(..., title="User Input",
                            description="The input message from the user, which will be moderated according to the defined settings.")
    character: str = Field("Curious Cow", title="Character",
                           description="Specifies the character from children's books that is speaking. Selected based on the moderated input.")
    moderation: ContentModeration = Field(..., title="Content Moderation",
                                          description="Defines the moderation parameters for screening user input, ensuring content safety.")
    poem: str = Field(..., min_length=50, title="Poem",
                      description="The moderated, original poem from the character, crafted in response to the user's input. "
                                  "If the moderation level is over 3 write a poem correcting the child's behavior.")


class ConversationAggregate(AbstractAggregate):
    def __init__(self, actor_system: "ActorSystem"):
        super().__init__(actor_system)
        self.context = Munch({"intent": None, "entity": None})
        self.state = "initial"

    async def handle_recognize_intent_command(self, command: ddd.RecognizeIntentCommand):
        # Simulate intent recognition logic
        intent = instance(ddd.IntentRecognizedEvent, command.user_input)  # Assume instance() magically does the job
        self.apply_event(intent)

    async def handle_recognize_entity_command(self, command: ddd.RecognizeEntityCommand):
        # Simulate entity recognition logic
        entity = instance(ddd.EntityRecognizedEvent, command.user_input)  # Assume instance() works similarly
        self.apply_event(entity)

    async def handle_update_context_command(self, command: ddd.UpdateContextCommand):
        if command.replace:
            self.context = command.updates
        else:
            self.context.update(command.updates)
        self.apply_event(ddd.ContextUpdatedEvent(content="Context updated"))

    async def handle_transition_state_command(self, command: ddd.TransitionStateCommand):
        self.state = command.new_state
        self.apply_event(ddd.StateTransitionEvent(content=f"Transitioned to {self.state} state"))

    async def handle_generate_response_command(self, command: ddd.GenerateResponseCommand):
        # Simplified response generation logic based on intent
        if self.context.get("intent") == "greeting":
            response = "Hello! How can I assist you today?"
        elif self.context.get("intent") == "inquiry":
            response = "What information are you seeking?"
        else:
            response = "I'm sorry, could you rephrase that?"

        self.apply_event(ddd.ResponseGeneratedEvent(content=response))

    async def handle_user_query_command(self, command: ddd.HandleUserQueryCommand):
        # Process user query and potentially invoke other commands based on the query
        self.apply_event(ddd.UserInputReceivedEvent(content=command.query))
        # Example: Recognize intent from the user query
        await self.handle_recognize_intent_command(ddd.RecognizeIntentCommand(user_input=command.query))
        # Generate a response based on recognized intent
        await self.handle_generate_response_command(ddd.GenerateResponseCommand(intent=self.context.get("intent", "")))

    async def handle_user_input(self, event: ddd.UserInputReceivedEvent) -> CharacterMessage:
        init_dspy()
        return CharacterMessage.to_inst(event.content)

    def apply_event(self, event):
        if isinstance(event, ddd.IntentRecognizedEvent):
            self.context['intent'] = event.intent_name
        elif isinstance(event, ddd.EntityRecognizedEvent):
            self.context['entity'] = event.entity_name
        # Include handling for other event types as needed
        else:
            # It's helpful to log or handle the case where an event is not recognized
            print(f"Unhandled event type: {type(event)}")
