from dspygen.modules.business_dev_consultant import business_dev_consultant_call
from dspygen.modules.mermaid_js_module import mermaid_js_call, MermaidDiagramType

event_storm_model_prompt = """Generate a comprehensive MermaidJS diagram that encapsulates our entire system's 
architecture based on Domain-Driven Design. Include the following elements, ensuring to illustrate the interactions 
and workflows where applicable: Domain Events (TaskStartedEvent, TaskCompletedEvent, TaskFailedEvent, 
ExternalEventOccurredEvent), External Events (ExternalSystemUpdatedEvent, RegulationAmendedEvent, 
ThirdPartyNotificationEvent, DataReceivedEvent, PartnerNotificationEvent, ServiceDownEvent, SecurityAlertEvent), 
Commands (StartProcessCommand, StopProcessCommand, ExecuteActivityCommand, InvokePartnerCommand, 
ReceiveFromPartnerCommand, HandleFaultCommand, SaveProcessInstanceCommand, LoadProcessInstanceCommand), 
Queries (GetProcessStatusQuery, GetActivityDetailsQuery, GetVariableValueQuery, GetProcessMetricsQuery), Aggregates (
ProcessExecutionAggregate, ActivityExecutionAggregate, PartnerInteractionAggregate, ProcessInstanceAggregate), 
Policies (ExecutionPolicy, RetryPolicy, CompensationPolicy, FaultHandlingPolicy), Read Models (
ProcessSummaryReadModel, ActivityLogReadModel, VariableSnapshotReadModel, ProcessInstanceDetailsReadModel), 
Views (ProcessOverviewView, TaskDetailsView, UserDashboardView, ErrorLogView), UI Events (ButtonClickEvent, 
FormSubmissionEvent, TaskCompletionEvent, UserInteractionEvent), Sagas (ProcessExecutionSaga, CompensationSaga, 
FaultHandlingSaga), Integration Events (ServiceInvocationEvent, DataTransferEvent, PartnerInteractionEvent, 
IntegrationEvent), Exceptions (ExecutionFailureException, DataProcessingException, IntegrationException, 
SystemException), Value Objects (ProcessIDValueObject, ActivityDetailsValueObject, PartnerDetailsValueObject, 
VariableValueObject), and Tasks (DataValidationTask, ServiceInvocationTask, ErrorHandlingTask, IntegrationTask). The 
diagram should clearly define the system's bounded contexts, aggregates, and how various events trigger state changes 
or processes within our architecture."""

concepts_to_visualize = [
    {"concept_name": "Bounded Contexts", "diagram_type": "STATE_DIAGRAM", "description": "Visualize the various bounded contexts within the system, highlighting their responsibilities and interactions."},
    {"concept_name": "Domain Events", "diagram_type": "SEQUENCE_DIAGRAM", "description": "Sequence diagram showing the flow and handling of domain events across bounded contexts."},
    {"concept_name": "Entities and Aggregates", "diagram_type": "CLASS_DIAGRAM", "description": "Class diagram representing entities and aggregates, including their relationships and boundaries."},
    {"concept_name": "Event Sourcing and CQRS", "diagram_type": "flowchart", "description": "Flowchart illustrating the Event Sourcing and CQRS patterns applied within the system for state management and read/write operations."},
    {"concept_name": "Integration and Messaging Channels", "diagram_type": "erDiagram", "description": "ER diagram mapping out the integration points and messaging channels between bounded contexts and external systems."},
    {"concept_name": "Reactive Components", "diagram_type": "CLASS_DIAGRAM", "description": "Class diagram for the architecture of reactive components, showcasing reactive streams and back-pressure handling."},
    {"concept_name": "Sagas and Process Managers", "diagram_type": "SEQUENCE_DIAGRAM", "description": "Sequence diagram for sagas and process managers orchestrating long-running processes and transactions."},
    {"concept_name": "Policy and Rule Enforcement", "diagram_type": "STATE_DIAGRAM", "description": "State diagram visualizing policy and rule enforcement in the system, including validation and business rules."},
    {"concept_name": "Read Models and Projections", "diagram_type": "erDiagram", "description": "Diagram the structure of read models and projections, showing how they are updated via event listeners."},
    {"concept_name": "UI and External Interfaces", "diagram_type": "mindmap", "description": "Mindmap of the system's UI and external interfaces, detailing how they interact with the core domain."},
    {"concept_name": "Testing and Simulation of Reactive Systems", "diagram_type": "gantt", "description": "Gantt chart outlining the testing phases, including unit testing, integration testing, and end-to-end testing of reactive systems."},
    {"concept_name": "Scalability and Resilience Patterns", "diagram_type": "quadrantChart", "description": "Quadrant chart evaluating the application of scalability and resilience patterns like circuit breakers, retries, and responsive scaling."}
]

def generate_all_diagrams():
    for concept in concepts_to_visualize:
        # Assuming mermaid_js_call is adapted to handle these inputs.
        print(f"Generating diagram for: {concept['concept_name']}")
        diagram_output = mermaid_js_call(prompt=f"{concept['description']}\n{event_storm_model_prompt}", mermaid_type=MermaidDiagramType.STATE_DIAGRAM)
        # Here, you would write diagram_output to a file or otherwise process it.
        # Example file name format: "{concept_name}.mmd" (replace spaces with underscores in concept_name for the file name)
        file_name = f"{concept['concept_name'].replace(' ', '_')}.mmd"
        with open(file_name, 'w') as file:
            file.write(diagram_output)

def main():
    from dspygen.utils.dspy_tools import init_dspy
    init_dspy(model="gpt-4", max_tokens=5000)

    generate_all_diagrams()

    # advice = business_dev_consultant_call(prompt="I need you to write a Synthetic Design for Lean Six Sigma BPMN to BPEL workflow execution engine project charter.")
    # print(advice)


if __name__ == '__main__':
    main()
