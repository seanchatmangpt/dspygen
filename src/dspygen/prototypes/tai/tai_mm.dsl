stateDiagram-v2
    [*] --> SimulationBusiness: Initiate
    SimulationBusiness --> TypesOfSimulations: Define Scope
    SimulationBusiness --> PrimaryClients: Identify Clients
    SimulationBusiness --> KeyProjects: Project Planning
    SimulationBusiness --> InternalSupportDivisions: Organize Support

    TypesOfSimulations --> MilitaryTrainingSimulators: Focus Military
    TypesOfSimulations --> VehicleOperationSimulators: Focus Vehicles
    TypesOfSimulations --> EnvironmentalSimulators: Focus Environment
    MilitaryTrainingSimulators --> VehicleOperationSimulators: Cross-Application
    VehicleOperationSimulators --> EnvironmentalSimulators: Cross-Application
    EnvironmentalSimulators --> MilitaryTrainingSimulators: Cross-Application

    PrimaryClients --> DepartmentOfDefense: Engage DoD
    PrimaryClients --> NASA: Engage NASA
    PrimaryClients --> DepartmentOfTransportation: Engage DOT
    DepartmentOfDefense --> NASA: Cross-Engagement
    NASA --> DepartmentOfTransportation: Cross-Engagement
    DepartmentOfTransportation --> DepartmentOfDefense: Cross-Engagement

    KeyProjects --> NavyAmphibiousVehicleSimulators: Navy Focus
    KeyProjects --> MarineCorpsTacticalSimulators: Marines Focus
    KeyProjects --> AirForceFlightSimulators: Air Force Focus
    NavyAmphibiousVehicleSimulators --> MarineCorpsTacticalSimulators: Transition Projects
    MarineCorpsTacticalSimulators --> AirForceFlightSimulators: Transition Projects
    AirForceFlightSimulators --> NavyAmphibiousVehicleSimulators: Transition Projects

    InternalSupportDivisions --> ResearchAndDevelopment: R&D Support
    InternalSupportDivisions --> TechnicalServices: Technical Support
    InternalSupportDivisions --> MarketingAndSales: Market Outreach
    InternalSupportDivisions --> CustomerSupport: Support Services
    ResearchAndDevelopment --> TechnicalServices: Develop to Support
    TechnicalServices --> MarketingAndSales: Support to Market
    MarketingAndSales --> CustomerSupport: Market to Support
    CustomerSupport --> ResearchAndDevelopment: Feedback Loop

    %% Returning to Start
    MilitaryTrainingSimulators --> SimulationBusiness: Update Scope
    DepartmentOfDefense --> SimulationBusiness: Update Client List
    NavyAmphibiousVehicleSimulators --> SimulationBusiness: Update Project List
    ResearchAndDevelopment --> SimulationBusiness: R&D Feedback

    %% State Connections
    state TypesOfSimulations {
        MilitaryTrainingSimulators
        VehicleOperationSimulators
        EnvironmentalSimulators
    }
    state PrimaryClients {
        DepartmentOfDefense
        NASA
        DepartmentOfTransportation
    }
    state KeyProjects {
        NavyAmphibiousVehicleSimulators
        MarineCorpsTacticalSimulators
        AirForceFlightSimulators
    }
    state InternalSupportDivisions {
        ResearchAndDevelopment
        TechnicalServices
        MarketingAndSales
        CustomerSupport
    }
