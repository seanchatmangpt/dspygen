"""The BaseActor Module for Reactive Domain-Driven Design (RDDDY) Framework
---------------------------------------------------------------------

This module implements the core Actor abstraction within the RDDDY framework, providing a robust foundation for building reactive, domain-driven systems that are scalable, maintainable, and capable of handling complex, concurrent interactions. The Actor model encapsulates both state and behavior, allowing for asynchronous message passing as the primary means of communication between actors, thus fostering loose coupling and enhanced system resilience.

### Overview

Actors are the fundamental units of computation in the RDDDY framework. Each actor possesses a unique identity, a mailbox for message queuing, and a set of behaviors to handle incoming messages. The Actor module facilitates the creation, supervision, and coordination of actors within an ActorSystem, ensuring that messages are delivered and processed in a manner consistent with the system's domain-driven design principles.

### Multiline Calculus for Actor Behavior Specification

The operational semantics of actors within the RDDDY framework are formalized through a rigorous multiline calculus, which outlines the preconditions, postconditions, and invariants that govern actor behavior and interaction. This calculus serves as a contract, ensuring that actors behave correctly and predictably within their designated domain contexts.

#### Actor State Transition

Given an actor \(A\) with state \(s\) and a message \(m\), the state transition is defined as:

Precondition ( Pre Pre): 𝑠 ∈ 𝑆 s∈S and 𝑚 ∈ 𝑀 m∈M
Transition: 𝑇 ( 𝑠 , 𝑚 ) → 𝑠 ′ T(s,m)→s ′
Postcondition ( Post Post): 𝑠 ′ ∈ 𝑆 ′ s ′ ∈S ′

#### Message Handling

For a message \(m\) handled by the actor, leading to a state modification:

Precondition ( Pre Pre): 𝑠 ∈ 𝑆 s∈S and 𝑚 ∈ 𝑀 m∈M
Handling: 𝐻 ( 𝑚 , 𝑠 ) → 𝑠 ′ ′ H(m,s)→s ′′
Postcondition ( Post Post): 𝑠 ′ ′ ∈ 𝑆 ′ ′ s ′′ ∈S ′′

#### Invariant Maintenance

Ensuring system invariants \(I\) across transitions:

Invariant: 𝐼 ( 𝑆 ) ∧ 𝑇 ( 𝑠 , 𝑚 ) → 𝑠 ′ ⇒ 𝐼 ( 𝑆 ′ ) I(S)∧T(s,m)→s ′ ⇒I(S ′ )

#### Domain-Specific Assertions

Linking actor state transitions to domain logic:

Precondition ( Pre Pre): Δ ( 𝑠 ) Δ(s) and 𝛿 ( 𝑚 ) δ(m)
Domain Logic: 𝐷 ( 𝑠 , 𝑚 ) → Δ ( 𝑠 ′ ) D(s,m)→Δ(s ′ )
Postcondition ( Post Post): Δ ′ ( 𝑠 ′ ) Δ ′ (s ′ )

### Purpose

This calculus not only specifies the expected behavior of actors in response to messages but also integrates domain-specific knowledge, ensuring that actors operate in alignment with the broader domain-driven objectives of the system. By adhering to these specifications, the Actor module provides a reliable and expressive framework for developing systems that are both technically sound and closely aligned with domain requirements.

### Usage

Developers should implement actor behaviors in accordance with the outlined calculus, ensuring that each actor's implementation respects the preconditions, postconditions, and domain-specific assertions relevant to their system's domain logic. This approach facilitates the development of systems that are not only functionally correct but also domain-compliant, thereby enhancing the value and applicability of the RDDDY framework in real-world scenarios.
"""
import asyncio
from collections.abc import Callable
from typing import TYPE_CHECKING, Optional, Type

import reactivex as rx
from loguru import logger
from reactivex import operators as ops
from reactivex.scheduler.eventloop import AsyncIOScheduler

from dspygen.rdddy.base_event import BaseEvent
from dspygen.rdddy.base_message import *

if TYPE_CHECKING:
    from dspygen.rdddy.actor_system import ActorSystem


class BaseActor:
    """Represents an actor within the RDDDY framework.

    Actors are fundamental units of computation in the RDDDY framework, encapsulating both state and behavior.
    They communicate asynchronously through message passing, promoting loose coupling and system resilience.

    Args:
        actor_system (ActorSystem): The ActorSystem to which the actor belongs.
        actor_id (int, optional): The unique identifier of the actor. Defaults to None.

    Attributes:
        actor_system (ActorSystem): The ActorSystem to which the actor belongs.
        actor_id (int): The unique identifier of the actor.
        mailbox (Subject): A subject for message queuing.
        handlers (dict): A mapping of message types to corresponding handler methods.

    Methods:
        start(scheduler): Starts the actor's mailbox processing loop.
        on_next(message): Callback function for processing incoming messages.
        on_error(error): Callback function for handling errors in the actor's mailbox.
        on_completed(): Callback function when the actor's mailbox stream completes.
        receive(message): Processes an incoming message.
        send(recipient_id, message): Sends a message to another actor.
        publish(message): Publishes a message to the actor system.
        map_handlers(): Maps message types to corresponding handler methods.
    """

    def __init__(self, actor_system: "ActorSystem", actor_id: Optional[int] = None):
        self.actor_system = actor_system
        self.actor_id = actor_id or id(self)
        self.mailbox = rx.subject.Subject()
        self.handlers = self.map_handlers()

    async def start(self, scheduler: AsyncIOScheduler):
        """Initiates the processing loop for the actor's mailbox, ensuring asynchronous message handling.

        Preconditions (Pre):
            - The actor's mailbox must be initialized.
            - A valid scheduler must be provided.

        Transition (T):
            - Initiates the processing loop for the actor's mailbox, enabling asynchronous message handling.

        Postconditions (Post):
            - The actor's mailbox processing loop has started successfully.

        Args:
            scheduler: An asynchronous scheduler used to control the execution of tasks.

        """
        self.mailbox.pipe(ops.observe_on(scheduler)).subscribe(
            on_next=self.on_next,  # Synchronous wrapper for async handler
            on_error=self.on_error,
            on_completed=self.on_completed,
        )
        logger.info(f"Actor {self.actor_id} started")

    def on_next(self, message: BaseMessage):
        """Handles the next incoming message in the actor's mailbox.

        Preconditions (Pre):
            - The incoming message must be a valid instance of the Message class.

        Transition (T):
            - Processes the incoming message asynchronously.

        Postconditions (Post):
            - The incoming message has been processed by the actor.

        Args:
            message (BaseMessage): The incoming message to be processed.
        """
        # Schedule the async handler as a new task
        # logger.debug(f"Actor {self.actor_id} received message: {message}")
        asyncio.create_task(self.receive(message))

    def on_error(self, error):
        """Handles errors that occur in the actor's mailbox processing.

        Preconditions (Pre):
            - None

        Transition (T):
            - Handles the error generated during mailbox processing.

        Postconditions (Post):
            - The error has been handled, and appropriate action has been taken.

        Args:
            error: The error object representing the error that occurred.
        """
        logger.error(f"Error in actor {self.actor_id} mailbox: {error}")

    def on_completed(self):
        """Handles the completion of the actor's mailbox stream.

        Preconditions (Pre):
            - None

        Transition (T):
            - Handles the completion event of the actor's mailbox stream.

        Postconditions (Post):
            - The actor's mailbox stream has completed, and appropriate action has been taken.
        """
        # logger.debug(f"Actor {self.actor_id} mailbox stream completed")

    async def receive(self, message: BaseMessage):
        """Processes an incoming message received by the actor.

        Preconditions (Pre):
            - The incoming message must be a valid instance of the Message class.

        Transition (T):
            - Processes the incoming message asynchronously, invoking the appropriate handler method.

        Postconditions (Post):
            - The incoming message has been successfully processed by the actor.

        Args:
            message (BaseMessage): The incoming message to be processed.
        """
        try:
            handler = self.handlers.get(type(message))
            if handler:
                logger.debug(
                    f"Actor handling message: {message} with {handler.__name__}"
                )
                await handler(message)
        except Exception as e:
            error_message = f"Error in actor {self.actor_id} processing message: {e}"
            # Broadcast an error event through the actor system
            await self.publish(BaseEvent(content=error_message))
            logger.error(error_message)

    async def publish(self, message: BaseMessage):
        """Publishes a message to the actor system for distribution.

        Preconditions (Pre):
            - The message must be a valid instance of the Message class.

        Transition (T):
            - Publishes the message to the actor system for distribution.

        Postconditions (Post):
            - The message has been successfully published to the actor system.

        Args:
            message (BaseMessage): The message to be published.
        """
        if message.actor_id == -1:
            message.actor_id = self.actor_id

        await self.actor_system.publish(message)

    def map_handlers(self) -> dict[Type[BaseMessage], Callable]:
        """Maps message types to corresponding handler methods.

        Preconditions (Pre):
            - None

        Transition (T):
            - Iterates through the methods of the actor instance and identifies callable methods with annotations.
            - Maps message types to corresponding handler methods based on method annotations.

        Postconditions (Post):
            - A dictionary containing message types as keys and corresponding handler methods as values has been generated.
        """
        handlers = {}
        for name, method in inspect.getmembers(self):
            if callable(method) and hasattr(method, "__annotations__"):
                annotations = method.__annotations__
                for arg in annotations.values():
                    try:
                        if issubclass(arg, BaseMessage):
                            handlers[arg] = method
                    except TypeError:
                        pass
        del handlers[BaseMessage]
        return handlers
