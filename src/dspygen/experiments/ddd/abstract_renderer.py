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
            "TaskStartedEvent", "TaskCompletedEvent", "TaskFailedEvent",
            "ExternalEventOccurredEvent"
        ],
        "external_event_classnames": [
            "ExternalSystemUpdatedEvent",
            "RegulationAmendedEvent",
            "ThirdPartyNotificationEvent",
            "DataReceivedEvent",
            "PartnerNotificationEvent",
            "ServiceDownEvent",
            "SecurityAlertEvent"
        ],
        "command_classnames": [
            "StartProcessCommand", "StopProcessCommand", "ExecuteActivityCommand",
            "InvokePartnerCommand", "ReceiveFromPartnerCommand", "HandleFaultCommand",
            "SaveProcessInstanceCommand", "LoadProcessInstanceCommand"
        ],
        "query_classnames": [
            "GetProcessStatusQuery", "GetActivityDetailsQuery",
            "GetVariableValueQuery", "GetProcessMetricsQuery"
        ],
        "aggregate_classnames": [
            "ProcessExecutionAggregate", "ActivityExecutionAggregate",
            "PartnerInteractionAggregate", "ProcessInstanceAggregate"
        ],
        "policy_classnames": [
            "ExecutionPolicy", "RetryPolicy", "CompensationPolicy",
            "FaultHandlingPolicy"
        ],
        "read_model_classnames": [
            "ProcessSummaryReadModel", "ActivityLogReadModel",
            "VariableSnapshotReadModel", "ProcessInstanceDetailsReadModel"
        ],
        "view_classnames": [
            "ProcessOverviewView", "TaskDetailsView", "UserDashboardView",
            "ErrorLogView"
        ],
        "ui_event_classnames": [
            "ButtonClickEvent", "FormSubmissionEvent", "TaskCompletionEvent",
            "UserInteractionEvent"
        ],
        "saga_classnames": [
            "ProcessExecutionSaga", "CompensationSaga", "FaultHandlingSaga"
        ],
        "integration_event_classnames": [
            "ServiceInvocationEvent", "DataTransferEvent",
            "PartnerInteractionEvent", "IntegrationEvent"
        ],
        "exception_classnames": [
            "ExecutionFailureException", "DataProcessingException",
            "IntegrationException", "SystemException"
        ],
        "value_object_classnames": [
            "ProcessIDValueObject", "ActivityDetailsValueObject",
            "PartnerDetailsValueObject", "VariableValueObject"
        ],
        "task_classnames": [
            "DataValidationTask", "ServiceInvocationTask",
            "ErrorHandlingTask", "IntegrationTask"
        ]
    }

    event_storm_model = EventStormingDomainSpecificationModel.model_validate(
        event_storm_model_data
    )

    generate_class_definitions(event_storm_model)


if __name__ == "__main__":
    main()
