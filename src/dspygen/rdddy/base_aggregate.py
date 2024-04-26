from dspygen.rdddy.base_actor import BaseActor


class BaseAggregate(BaseActor):
    """Serves as the cornerstone of the domain model within the RDDDY framework, encapsulating a cluster of domain
    objects that are treated as a single unit for the purposes of data changes. An aggregate guarantees the
    consistency of changes to the domain objects it encompasses by enforcing invariants across the entire group,
    making it a critical element in maintaining the integrity and boundaries of the domain model. By extending
    BaseAggregate, developers can define the core logic that governs the state and behavior of an aggregate root
    and its associated entities and value objects. This approach not only aids in isolating domain logic from
    infrastructure concerns but also supports the implementation of complex business rules and transactions in a way
    that aligns with the principles of Domain-Driven Design. Aggregates are pivotal in ensuring that domain logic
    remains both encapsulated and correctly partitioned, facilitating a clear and maintainable domain model that can
    evolve over time with the business requirements."""
