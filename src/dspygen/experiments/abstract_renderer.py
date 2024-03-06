from dspygen.rdddy.event_storm_domain_specification_model import EventStormingDomainSpecificationModel
from dspygen.typetemp.template.typed_template import TypedTemplate

base_class_mapping = {
    "domain_event_classnames": "AbstractEvent",
    "external_event_classnames": "AbstractEvent",
    "command_classnames": "AbstractCommand",
    "query_classnames": "AbstractQuery",
    "aggregate_classnames": "AbstractAggregate",
    "policy_classnames": "AbstractPolicy",
    "read_model_classnames": "AbstractReadModel",
    "view_classnames": "AbstractView",
    "ui_event_classnames": "AbstractEvent",
    "saga_classnames": "AbstractSaga",
    "integration_event_classnames": "AbstractEvent",
    "exception_classnames": "DomainException",
    "value_object_classnames": "AbstractValueObject",
    "task_classnames": "AbstractTask",
}


class GenRDDDYClassTemplate(TypedTemplate):
    source = """from dspygen.rdddy.{{ base_class_name | underscore }} import {{ base_class_name }}


class {{ classname }}({{ base_class_name }}):
    \"\"\"Generated class for {{ classname }}, inheriting from {{ base_class_name }}.\"\"\"
    
"""
    to = "{{ base_class_name | underscore }}/{{ classname | underscore }}.py"


def generate_class_definitions(model: EventStormingDomainSpecificationModel):
    for attr, base_class_name in base_class_mapping.items():
        classnames = getattr(model, attr, [])
        for classname in classnames:
            tmpl = GenRDDDYClassTemplate(
                base_class_name=base_class_name, classname=classname
            )()


def main():
    event_storm_model_data = {
        "domain_event_classnames": [
            "OrderPlaced",
            "PaymentProcessed",
            "InventoryUpdated",
        ],
        "external_event_classnames": [
            "ExternalPaymentConfirmation",
            "SupplierInventoryUpdate",
            "SupplierInventoryConfirmation",
        ],
        "command_classnames": ["PlaceOrder", "ProcessPayment", "UpdateInventory"],
        "query_classnames": ["GetOrderDetails", "ListBooks", "CheckOrderStatus"],
        "aggregate_classnames": [
            "OrderAggregate",
            "BookAggregate",
            "CustomerAggregate",
        ],
        "policy_classnames": [
            "OrderCancellationPolicy",
            "RefundPolicy",
            "ShippingPolicy",
        ],
        "read_model_classnames": [
            "OrderSummaryReadModel",
            "BookCatalogReadModel",
            "CustomerOrderHistoryReadModel",
        ],
        "view_classnames": ["OrderDetailsView", "BookListView", "CustomerProfileView"],
        "ui_event_classnames": [
            "AddToCartButtonClick",
            "CheckoutFormSubmitted",
            "OrderHistoryPageLoaded",
        ],
        "saga_classnames": [
            "OrderFulfillmentSaga",
            "PaymentProcessingSaga",
            "BookRestockSaga",
        ],
        "integration_event_classnames": [
            "OrderPlacedIntegrationEvent",
            "PaymentProcessedIntegrationEvent",
            "InventoryUpdatedIntegrationEvent",
        ],
        "exception_classnames": [
            "OrderNotFoundException",
            "PaymentDeclinedException",
            "BookOutOfStockException",
        ],
        "value_object_classnames": ["Address", "Price", "Quantity"],
        "task_classnames": [
            "ValidateOrder",
            "CalculateShippingCosts",
            "SendOrderConfirmationEmail",
        ],
    }

    event_storm_model = EventStormingDomainSpecificationModel.model_validate(
        event_storm_model_data
    )

    generate_class_definitions(event_storm_model)


if __name__ == "__main__":
    main()
