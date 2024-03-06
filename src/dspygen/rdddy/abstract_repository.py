from dspygen.rdddy.abstract_actor import AbstractActor


class AbstractRepository(AbstractActor):
    """Provides a template for implementing repositories, which abstract the logic required to access domain
    aggregates from the underlying storage mechanism. It serves as a bridge between the domain model and data
    management layers, enabling the decoupling of domain logic from data persistence concerns. By creating subclasses
    of AbstractRepository, developers can ensure smooth interactions with the domain entities, offering a clean,
    cohesive API for querying and persisting domain objects, thereby supporting the principles of domain-driven
    design."""

    pass
