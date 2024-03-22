from pydantic import Field, BaseModel

from dspygen.rdddy.abstract_event import AbstractEvent
from dspygen.utils.dspy_tools import init_dspy


class EventStormingDomainSpecificationModel(BaseModel):
    """Integrates Event Storming with RDDDY and DFLSS to capture and analyze domain complexities through events, commands, and queries, using Hoare logic for correctness. It serves as a repository for interactions identified in Event Storming, enhancing system responsiveness and process efficiency. This model educates on designing and verifying systems aligned with domain requirements and operational excellence. CamelCase only. """

    domain_events: list[AbstractEvent] = Field(
        ...,
        min_length=3,
        description="List of domain events triggering system reactions. Examples: 'OrderPlaced', 'PaymentProcessed', 'InventoryUpdated'.",
    )

def main():
    init_dspy()

    inst = instance(EventStormingDomainSpecificationModel, "Shipping System")
    print(inst)


if __name__ == '__main__':
    main()
