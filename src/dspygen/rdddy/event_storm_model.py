from pydantic import Field, BaseModel

from dspygen.rdddy.base_event import BaseEvent
from dspygen.utils.dspy_tools import init_dspy


class EventStormingDomainSpecificationModel(BaseModel):
    """Integrates Event Storming with RDDDY and DFLSS to capture and analyze domain complexities through events, commands, and queries, using Hoare logic for correctness. It serves as a repository for interactions identified in Event Storming, enhancing system responsiveness and process efficiency. This model educates on designing and verifying systems aligned with domain requirements and operational excellence. CamelCase only. """

    domain_events: list[BaseEvent] = Field(
        ...,
        min_length=3,
        description="List of domain events triggering system reactions. Examples: 'OrderPlaced', 'PaymentProcessed', 'InventoryUpdated'.",
    )

def main():
    init_dspy()

    from dspygen.modules.gen_pydantic_instance import instance
    inst = instance(EventStormingDomainSpecificationModel, "Shipping System")
    print(inst)


if __name__ == '__main__':
    main()
