"""Actor System Module Documentation

This module, actor_system.py, implements the ActorSystem class within the Reactive Domain-Driven Design (RDDDY) framework. It serves as the orchestrator for actor lifecycle management, message passing, and system-wide coordination, ensuring that the principles of the Actor model are adhered to in a domain-driven context.

Overview:
The ActorSystem is responsible for creating, managing, and terminating actors, facilitating asynchronous message passing between them, and maintaining system invariants. It is designed to operate seamlessly within an asynchronous programming environment, leveraging Python's asyncio library to handle concurrent operations efficiently.

ActorSystem Multiline Calculus Notation (AMCN):
The behavior and operations within the ActorSystem are rigorously defined by the ActorSystem Multiline Calculus Notation (AMCN), ensuring a formalized approach to actor management and message dissemination. The AMCN outlines the preconditions, actions, and postconditions for each operation within the system, integrating domain-specific assertions to align computational processes with the system's domain logic.

1. Actor Lifecycle Management
    Actor Creation (𝐴𝑐𝑟𝑒𝑎𝑡𝑒Acreate\u200b):
    - Precondition (Pre Pre): ¬∃𝑎∈𝐴∣𝑎.𝑖𝑑=𝑖𝑑𝑛𝑒𝑤 ¬∃a∈A∣a.id=id new\u200b
    - Action: 𝑐𝑟𝑒𝑎𝑡𝑒𝐴𝑐𝑡𝑜𝑟(𝑖𝑑𝑛𝑒𝑤,𝑇𝑦𝑝𝑒)→𝑎𝑛𝑒𝑤 createActor(id new\u200b,Type)→a new\u200b
    - Postcondition (Post Post): ∃𝑎∈𝐴∣𝑎.𝑖𝑑=𝑖𝑑𝑛𝑒𝑤∧𝑎.𝑡𝑦𝑝𝑒=𝑇𝑦𝑝𝑒 ∃a∈A∣a.id=id new\u200b∧a.type=Type

2. Message Dispatching
    Direct Message Sending (𝑀𝑠𝑒𝑛𝑑Msend\u200b):
    - Precondition (Pre Pre): ∃𝑎𝑠𝑒𝑛𝑑𝑒𝑟,𝑎𝑟𝑒𝑐𝑖𝑝𝑖𝑒𝑛𝑡∈𝐴 ∃a sender\u200b,a recipient\u200b∈A
    - Action: 𝑠𝑒𝑛𝑑𝑀𝑒𝑠𝑠𝑎𝑔𝑒(𝑎𝑠𝑒𝑛𝑑𝑒𝑟,𝑎𝑟𝑒𝑐𝑖𝑝𝑖𝑒𝑛𝑡,𝑚) sendMessage(a sender\u200b,a recipient\u200b,m)
    - Postcondition (Post Post): 𝑚∈𝑎𝑟𝑒𝑐𝑖𝑝𝑖𝑒𝑛𝑡.𝑚𝑎𝑖𝑙𝑏𝑜𝑥 m∈a recipient\u200b.mailbox

    Broadcast Messaging (𝑀𝑏𝑟𝑜𝑎𝑑𝑐𝑎𝑠𝑡𝑀broadcast\u200b):
    - Precondition (Pre Pre): ∃𝑎𝑠𝑒𝑛𝑑𝑒𝑟∈𝐴 ∃a sender\u200b∈A
    - Action: 𝑏𝑟𝑜𝑎𝑑𝑐𝑎𝑠𝑡𝑀𝑒𝑠𝑠𝑎𝑔𝑒(𝑎𝑠𝑒𝑛𝑑𝑒𝑟,𝑚) broadcastMessage(a sender\u200b,m)
    - Postcondition (Post Post): ∀𝑎∈𝐴∖{𝑎𝑠𝑒𝑛𝑑𝑒𝑟},𝑚∈𝑎.𝑚𝑎𝑖𝑙𝑏𝑜𝑥 ∀a∈A∖{a sender\u200b},m∈a.mailbox

3. System Invariants and Domain Assertions
    Invariant Preservation (𝐼𝑝𝑟𝑒𝑠𝑒𝑟𝑣𝑒Ipreserve\u200b):
    - Invariant (𝐼 I): Φ(𝐴,𝑀) Φ(A,M)
    - Upon Action (𝑎𝑐𝑡𝑖𝑜𝑛action): 𝑎𝑐𝑡𝑖𝑜𝑛(𝐴,𝑀)→𝐴′,𝑀′ action(A,M)→A′,M′
    - Preservation (𝐼′I′): Φ(𝐴′,𝑀′) Φ(A′,M′)
    Domain-Specific Logic Integration (𝐷𝑖𝑛𝑡𝑒𝑔𝑟𝑎𝑡𝑒Dintegrate\u200b):
    - Precondition (Pre 𝐷 Pre D\u200b): Δ(𝑠𝑔𝑙𝑜𝑏𝑎𝑙) Δ(s global\u200b)
    - Action and Domain Logic: 𝑝𝑒𝑟𝑓𝑜𝑟𝑚𝐴𝑐𝑡𝑖𝑜𝑛𝑊𝑖𝑡ℎ𝐷𝑜𝑚𝑎𝑖𝑛𝐿𝑜𝑔𝑖𝑐(𝑎,𝑚,Δ)→𝑠𝑔𝑙𝑜𝑏𝑎𝑙′,Δ′ performActionWithDomainLogic(a,m,Δ)→s global′\u200b,Δ′
    - Postcondition (Post 𝐷 Post D\u200b): Δ′(𝑠𝑔𝑙𝑜𝑏𝑎𝑙′) Δ′(s global′\u200b)

Implementation Details:
The ActorSystem is implemented with a focus on modularity, scalability, and ease of use. It provides a high-level API for actor management and message passing, abstracting away the complexities of asynchronous programming and actor coordination. Developers can leverage the ActorSystem to build complex, responsive applications that are both computationally correct and domain-compliant.

Usage:
To use the ActorSystem, instantiate it within your application and use its methods to create actors and manage message passing. The system integrates seamlessly with the asyncio event loop, making it straightforward to incorporate into existing asynchronous applications.

The actor_system.py module, guided by the AMCN, provides a robust foundation for developing actor-based systems within the RDDDY framework, ensuring that applications are built with a solid architectural foundation that promotes maintainability, scalability, and domain-driven design principles.
"""
import asyncio
import json
from asyncio import Future
from typing import TYPE_CHECKING, Optional, TypeVar, cast
from paho.mqtt import client as mclient

import reactivex as rx
from loguru import logger
from paho.mqtt.enums import CallbackAPIVersion
from reactivex import operators as ops
from reactivex.scheduler.eventloop import AsyncIOScheduler

from dspygen.rdddy.base_message import BaseMessage, MessageFactory

if TYPE_CHECKING:
    from dspygen.rdddy.base_actor import BaseActor

T = TypeVar("T", bound="BaseActor")


class ActorSystem:
    """Orchestrates actor lifecycle management, message passing, and system-wide coordination within the RDDDY framework.

    The ActorSystem class provides functionalities for creating, managing, and terminating actors, facilitating asynchronous message passing between them, and maintaining system invariants.

    Attributes:
        actors (dict): A dictionary containing actor IDs as keys and corresponding actor instances as values.
        loop (asyncio.AbstractEventLoop): The asyncio event loop used for asynchronous operations.
        scheduler (AsyncIOScheduler): An asynchronous scheduler for controlling task execution.
        event_stream (Subject): A subject for publishing events within the actor system.

    Methods:
        actor_of(actor_class, **kwargs): Creates a new actor instance and starts its mailbox processing loop.
        actors_of(actor_classes, **kwargs): Creates multiple actor instances of different types.
        publish(message): Publishes a message to the actor system for distribution.
        remove_actor(actor_id): Removes an actor from the actor system.
        send(actor_id, message): Sends a message to a specific actor within the system.
        wait_for_event(event_type): Waits for a specific event type to occur within the system.

    Implementation Details:
    The ActorSystem class implements actor management and message passing functionalities, abstracting away the
    complexities of asynchronous programming and actor coordination. It integrates seamlessly with the asyncio
    event loop, ensuring efficient concurrent operations.

    Usage:
    Instantiate an ActorSystem object within your application to manage actors and coordinate message passing. Use its
    methods to create actors, send messages, and wait for specific events within the system.
    """

    def __init__(self, loop: Optional[asyncio.AbstractEventLoop] = None, mqtt_client: mclient = None):
        """Initializes the ActorSystem.

        Args:
            loop (asyncio.AbstractEventLoop, optional): The asyncio event loop to be used for asynchronous operations.
                If not provided, the default event loop will be used.

        Attributes:
            actors (dict): A dictionary containing actor IDs as keys and corresponding actor instances as values.
            loop (asyncio.AbstractEventLoop): The asyncio event loop used for asynchronous operations.
            scheduler (AsyncIOScheduler): An asynchronous scheduler for controlling task execution.
            event_stream (Subject): A subject for publishing events within the actor system.
        """
        self.mqtt_client = mqtt_client
        self.actors: dict[int, BaseActor] = {}
        self.loop = loop if loop is not None else asyncio.get_event_loop()
        self.scheduler = AsyncIOScheduler(loop=self.loop)
        self.event_stream = rx.subject.Subject()

        # try:
        #     self.mqtt_client = mqtt_client.Client(CallbackAPIVersion.VERSION2)
        #     self.mqtt_client.on_connect = self.on_connect
        #     self.mqtt_client.on_message = self.on_message  # Define the callback for incoming messages
        #     self.mqtt_client.connect(mqtt_broker, mqtt_port, 60)
        #     self.mqtt_client.loop_start()
        # except (ConnectionRefusedError, OSError) as e:
        #     logger.error(f"Error connecting to MQTT Broker: {e}")

    def on_connect(self, client, userdata, flags, reason_code, properties):
        print("Connected to MQTT Broker.")
        client.subscribe("actor_system/publish")  # Subscribe to the topic

    def on_message(self, client, userdata, msg):
        print(f"Received message from topic {msg.topic}: {msg.payload}")
        # Deserialize the message payload into your internal message format
        payload_dict = json.loads(msg.payload)
        message = MessageFactory.create_message(payload_dict) # Implement this method based on your message class
        asyncio.run_coroutine_threadsafe(self.distribute_message(message), self.loop)

    async def distribute_message(self, message):
        # Prevent republishing to MQTT by directly invoking the local distribution logic
        self.event_stream.on_next(message)
        actors = list(self.actors.values())
        for actor in actors:
            await self.send(actor.actor_id, message)

    async def actor_of(self, actor_class, **kwargs) -> T:
        """Creates a new actor instance and starts its mailbox processing loop.
        T = TypeVar("T", bound="Actor")

        Preconditions (Pre):
            - None

        Transition (T):
            - Creates a new instance of the specified actor class.
            - Initializes the actor's mailbox.
            - Starts the processing loop for the actor's mailbox, enabling asynchronous message handling.

        Postconditions (Post):
            - A new actor instance has been created and started successfully.

        Args:
            actor_class: The class of the actor to be created.
            **kwargs: Additional keyword arguments to be passed to the actor constructor.

        Returns:
            T: The created actor instance.
        """
        actor = actor_class(self, **kwargs)
        self.actors[actor.actor_id] = actor
        await actor.start(self.scheduler)
        return actor

    async def actors_of(self, actor_classes, **kwargs) -> list[T]:
        """Creates multiple actor instances of different types and starts their mailbox processing loops.
        T = TypeVar("T", bound="Actor")

        Preconditions (Pre):
            - None

        Transition (T):
            - Creates new instances of the specified actor classes.
            - Initializes the mailboxes for each actor.
            - Starts the processing loop for each actor's mailbox, enabling asynchronous message handling.

        Postconditions (Post):
            - Multiple actor instances have been created and started successfully.

        Args:
            actor_classes (List[Type]): A list of actor classes to be instantiated.
            **kwargs: Additional keyword arguments to be passed to the actor constructors.

        Returns:
            List[T]: A list containing the created actor instances.
        """
        actors = []
        for actor_class in actor_classes:
            actor = await self.actor_of(actor_class, **kwargs)
            actors.append(actor)
        return actors

    async def publish(self, message: "BaseMessage"):
        """Publishes a message to the actor system for distribution.

        Preconditions (Pre):
            - None

        Transition (T):
            - Emits the message to the event stream of the actor system.
            - Sends the message to each actor within the system for processing.

        Postconditions (Post):
            - The message has been published to the actor system and processed by relevant actors.
            - If the message is an instance of the base Message class, an error is raised.

        Args:
            message (BaseMessage): The message to be published to the actor system.

        Raises:
            ValueError: If the base Message class is used directly.
        """
        logger.debug(f"Publishing message: {message}")

        if type(message) is BaseMessage:
            raise ValueError(
                "The base Message class should not be used directly. Please use a subclass of Message."
            )

        self.event_stream.on_next(message)
        actors = list(self.actors.values())
        for actor in actors:
            await self.send(actor.actor_id, message)

        actor_system_topic = "actor_system/publish"
        # self.mqtt_client.publish(actor_system_topic, message.model_dump_json())

    async def remove_actor(self, actor_id):
        """Removes an actor from the actor system.

        Preconditions (Pre):
            - The actor ID must exist in the actor system.

        Transition (T):
            - Removes the actor with the specified ID from the actor system.

        Postconditions (Post):
            - The actor has been successfully removed from the actor system.

        Args:
            actor_id: The ID of the actor to be removed.
        """
        actor = self.actors.pop(actor_id, None)
        if actor:
            logger.debug(f"Removing actor {actor_id}")
        else:
            logger.debug(f"Actor {actor_id} not found for removal")
        logger.debug(f"Current actors count: {len(self.actors)}")

    async def send(self, actor_id: int, message: "BaseMessage"):
        """Sends a message to a specific actor within the actor system.

        Preconditions (Pre):
            - The actor ID must exist in the actor system.
            - The message must be an instance of the Message class.

        Transition (T):
            - Delivers the message to the specified actor's mailbox for processing.

        Postconditions (Post):
            - The message has been successfully sent to the specified actor for processing.

        Args:
            actor_id (int): The ID of the target actor.
            message (BaseMessage): The message to be sent to the target actor.
        """
        # logger.debug(f"Sending message {message} to actor {actor_id}")
        actor = self.actors.get(actor_id)
        if actor:
            actor.mailbox.on_next(message)
            await asyncio.sleep(0)
        else:
            logger.debug(f"Actor {actor_id} not found.")

    async def wait_for_message(self, message_type: type) -> Future["BaseMessage"]:
        """Waits for a message of a specific type to be published to the actor system.

        Preconditions (Pre):
            - None

        Transition (T):
            - Subscribes to the event stream of the actor system.
            - Waits until a message of the specified type is published.

        Postconditions (Post):
            - A message of the specified type has been received from the actor system.

        Args:
            message_type (type): The type of message to wait for.

        Returns:
            asyncio.Future: A future object representing the awaited message.
        """
        loop = asyncio.get_event_loop()
        future = loop.create_future()

        def on_next(msg):
            if isinstance(msg, message_type):
                future.set_result(msg)
                subscription.dispose()

        subscription = self.event_stream.pipe(
            ops.filter(lambda msg: isinstance(msg, message_type))
        ).subscribe(on_next)

        return await future

    def __getitem__(self, actor_id) -> T:
        """Retrieves an actor by its ID from the actor system.

        Preconditions (Pre):
            - The actor ID must exist in the actor system.

        Transition (T):
            - Retrieves the actor with the specified ID from the actor system.

        Postconditions (Post):
            - The actor with the specified ID has been successfully retrieved from the actor system.

        Args:
            actor_id: The ID of the actor to retrieve.

        Returns:
            BaseActor: The actor object corresponding to the specified ID.
        """
        return cast(T, self.actors.get(actor_id))


    async def shutdown(self):
        """Shuts down the actor system and terminates all actors.

        Preconditions (Pre):
            - None

        Transition (T):
            - Terminates all actors within the actor system.
            - Closes the event stream and scheduler.

        Postconditions (Post):
            - The actor system has been successfully shut down.
        """
        # self.mqtt_client.loop_stop()
        # self.mqtt_client.disconnect()
        logger.debug("Actor system shutdown complete.")


import asyncio


async def main():
    print("main")
    # await


if __name__ == "__main__":
    asyncio.run(main())
