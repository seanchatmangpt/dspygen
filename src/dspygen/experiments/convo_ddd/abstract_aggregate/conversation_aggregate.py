import asyncio

from munch import Munch

import dspygen.experiments.convo_ddd as ddd

from dspygen.rdddy.abstract_aggregate import AbstractAggregate
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
                       description="Mandatory moderation intensity level, "
                                   "with 1 being the least restrictive and 5 the most. Focus on setting this value.")
    categories: List[str] = Field(default=[], min_length=0,
                                  description="List of specific content categories to moderate.")


class CharacterMessage(BaseModel, InstanceMixin):
    """
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
    level: int = Field(1, ge=1, le=5,
                       description="Mandatory moderation intensity level, "
                                   "with 1 being the least restrictive and 5 the most. Focus on setting this value.")
    poem: str = Field(..., title="Poem",
                      description="The moderated, original poem from the character, crafted in response to the user's input. "
                                  "If the moderation level is over 3 write a poem correcting the child's behavior.")


class ConversationAggregate(AbstractAggregate):
    def __init__(self, actor_system: "ActorSystem"):
        super().__init__(actor_system)
        self.context = Munch({"intent": None, "entity": None})
        self.state = "initial"

    async def handle_user_input(self, event: ddd.UserInputReceivedEvent) -> CharacterMessage:
        init_dspy()
        return CharacterMessage.to_inst(event.content)


async def main():
    """Main function"""
    asys = ActorSystem()
    agg = await asys.actor_of(ConversationAggregate)
    user_input = ddd.UserInputReceivedEvent(content="Hello, Curious Cow! How are you today? I want you ded")
    response = await agg.handle_user_input(user_input)
    print(response)


if __name__ == '__main__':
    asyncio.run(main())
