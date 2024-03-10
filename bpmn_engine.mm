graph LR
    subgraph ActorSystem
    AS(Actor System)
    BPMNEngine[BPMN Workflow Engine]
    ProcessManager[Process Manager]
    TaskExecutor[Task Executor]
    DecisionGateway[Decision Gateway]
    ExternalService[External Service Handler]
    EventListener[Event Listener]
    UserTaskHandler[User Task Handler]
    end

    AS -->|Deploys Model| BPMNEngine
    BPMNEngine -->|Starts Process| ProcessManager
    ProcessManager -->|Execute Task| TaskExecutor
    ProcessManager -->|Evaluate Decision| DecisionGateway
    TaskExecutor -->|Call External Service| ExternalService
    ProcessManager -->|User Task| UserTaskHandler
    UserTaskHandler -->|Complete Task| ProcessManager
    ExternalService -->|Callback Event| EventListener
    EventListener -->|Notify Completion| ProcessManager
    DecisionGateway -->|Decision Made| ProcessManager
    ProcessManager -->|Process Completed| BPMNEngine

    classDef actor fill:#f9f,stroke:#333,stroke-width:2px;
    class BPMNEngine,ProcessManager,TaskExecutor,DecisionGateway,ExternalService,EventListener,UserTaskHandler actor;
