from pydantic import BaseModel, Field
from typing import List, Optional


class Transition(BaseModel):
    """Transition model for Finite State Machine (FSM) based on the transitions library."""
    trigger: str = Field(..., description="The trigger method name for the transition")
    source: str = Field(..., description="The source state")
    dest: str = Field(..., description="The destination state")
    conditions: Optional[List[str]] = Field(None, description="List of conditions to check before transition")
    unless: Optional[List[str]] = Field(None, description="List of conditions to prevent transition")
    before: Optional[List[str]] = Field(None, description="List of methods to execute before transition")
    after: Optional[List[str]] = Field(None, description="List of methods to execute after transition")
    prepare: Optional[List[str]] = Field(None, description="List of methods to prepare for transition")


class StateMethod(BaseModel):
    name: str = Field(..., description="The method name")
    body: str = Field(..., description="The method body")


class FSMClassModel(BaseModel):
    """Class model for Finite State Machine (FSM) class. This model is used to generate FSM classes."""
    class_name: str = Field(..., description="The name of the FSM class")
    states: List[str] = Field(..., description="List of states")
    transitions: List[Transition] = Field(..., description="List of transitions", min_items=3)
    methods: List[StateMethod] = Field([], description="List of additional methods for the FSM class")


tmpl = """{% macro method_signature(method) %}
def {{ method.name }}(self):
        {{ method.body }}
{% endmacro %}

from enum import Enum, auto
from dspygen.mixin.fsm.fsm_mixin import FSMMixin, trigger


class {{ class_name }}State(Enum):
    {% for state in states %}
    {{ state.upper() }} = auto()
    {% endfor %}


class {{ class_name }}(FSMMixin):
    def __init__(self):
        super().setup_fsm({{ class_name }}State)
        # Initialize state-specific attributes if any

    {% for transition in transitions %}
    @trigger(
        source={{ class_name }}State.{{ transition.source.upper() }},
        dest={{ class_name }}State.{{ transition.dest.upper() }},
        conditions={{ transition.conditions }},
        unless={{ transition.unless }},
        before={{ transition.before }},
        after={{ transition.after }},
        prepare={{ transition.prepare }}
    )
    def {{ transition.trigger }}(self):
        print("Transitioning from {{ transition.source }} to {{ transition.dest }}")
        
    {% endfor -%}

    {% for method in methods %}
    {{ method_signature(method) }}
    {% endfor %}


def main():
    \"\"\"Main function\"\"\"
    fsm = {{ class_name }}()
    {% for transition in transitions %}
    fsm.{{ transition.trigger }}()  # Transition from {{ transition.source }} to {{ transition.dest }}
    {% endfor %}
    assert fsm.state == {{ class_name }}State.{{ transitions[-1].dest.upper() }}.name  # Verify final state


if __name__ == '__main__':
    main()    
"""


prompt = """Certainly! Here’s a Product Requirements Document (PRD) for a Revenue Operations (RevOps) Finite State Machine (FSM) Class Model. This document outlines the specifications and requirements necessary to develop a system that supports various revenue operations processes through a state machine framework.

---

### **Product Requirements Document: RevOps FSM Class Model**

#### **1. Product Overview**
The RevOps FSM Class Model will be a configurable state machine model designed to automate and manage revenue operations processes. This model will facilitate transitions through various stages of revenue operations, such as lead generation, order processing, revenue recognition, and customer retention strategies.

#### **2. Objectives**
- **Automate RevOps Workflows:** Automate transitions between different stages of revenue operations to increase efficiency and reduce manual intervention.
- **Enhance Visibility and Control:** Provide clear visibility into each stage of the operations process and enable better control over the progression of revenue-related activities.
- **Improve Compliance and Accuracy:** Ensure that all revenue operations comply with internal and external policies and standards, reducing errors and enhancing financial accuracy.
- **Facilitate Scalability:** Allow easy modifications and scalability to accommodate business growth or changes in operations.

#### **3. Target Audience**
- **RevOps Managers:** To oversee and manage the automated processes.
- **Sales and Marketing Teams:** To utilize insights and data flow for improving sales strategies.
- **Finance Departments:** To ensure accurate and compliant revenue reporting.

#### **4. Features and Specifications**

##### **4.1 State Definitions**
- **Stages of Revenue Lifecycle:** Define clear states representing each stage of the revenue lifecycle, from initial customer contact through to revenue realization and post-sale support.

##### **4.2 Transitions**
- **Trigger-based Progression:** Implement transitions that are triggered based on specific actions or criteria being met, ensuring smooth progression through revenue stages.
- **Conditional Logic:** Allow transitions to include conditions that must be met for the transition to execute, ensuring compliance and accuracy at each step.

##### **4.3 Methods and Actions**
- **Automated Actions:** Each transition should have associated actions that automate tasks such as data entry, notifications, or updates to CRM systems.
- **Manual Override:** Provide capabilities for users to manually override or initiate transitions when necessary, accompanied by appropriate security measures.

##### **4.4 Reporting and Analytics**
- **State Analytics:** Track and report on the time spent in each state, the outcomes of each state, and other key performance indicators.
- **Transition Metrics:** Analyze the effectiveness of each transition, including success rates and any issues encountered.

#### **5. Integration Requirements**
- **CRM Integration:** Seamlessly integrate with existing Customer Relationship Management (CRM) systems to synchronize data across platforms.
- **ERP Systems:** Connect with Enterprise Resource Planning (ERP) systems for real-time financial data and processing capabilities.
- **Data Security:** Ensure all integrations comply with data security standards and regulations.

#### **6. Usability and Accessibility**
- **User Interface:** Develop a user-friendly interface that allows non-technical users to configure and monitor the FSM without extensive training.
- **Documentation and Help:** Provide comprehensive user guides and online help resources to assist users in managing and troubleshooting the FSM.

#### **7. Compliance and Security**
- **Data Privacy:** Adhere to global data privacy laws such as GDPR and CCPA.
- **Audit Trails:** Implement detailed logging and audit trails for all actions and transitions to ensure traceability and accountability.

#### **8. Future Proofing**
- **Modularity and Scalability:** Design the FSM to be modular and easily scalable to accommodate additional states, transitions, and integrations as business needs evolve.

#### **9. Delivery Timeline**
- **Prototype Release:** 3 months post-approval.
- **Beta Testing:** 2 months post-prototype release.
- **Full Release:** 6 months post-approval.

---

This PRD sets a foundation for developing a robust and flexible RevOps FSM Class Model that meets the dynamic needs of revenue operations in an efficient and compliant manner.

RevopsFSM

Methods:
- log_transition
- notify_user
- update_data
- validate_input
- generate_report
- escalate_issue
- resolve_conflict
- archive_data
- purge_records
- send_notification
- update_status
- check_compliance
- verify_data
- process_payment
- update_inventory
- calculate_revenue
- generate_invoice
- send_receipt
- reconcile_accounts
- close_account
- refund_payment
- escalate_support
- resolve_dispute
- update_contract
- renew_subscription
- cancel_service
- initiate_return
- track_shipment
- update_customer_info
- schedule_delivery
- confirm_order
"""

revops_fsm = FSMClassModel(
    class_name="OrderProcessingFSM",
    states=["Order_Placed", "Order_Confirmed", "Payment_Processed", "Shipped", "Delivered", "Cancelled", "Returned"],
    transitions=[
        Transition(
            trigger="confirm_order",
            source="Order_Placed",
            dest="Order_Confirmed",
            conditions=["verify_data"],
            after=["send_notification"]
        ),
        Transition(
            trigger="process_payment",
            source="Order_Confirmed",
            dest="Payment_Processed",
            conditions=["check_compliance", "validate_input"],
            after=["generate_invoice", "send_receipt"]
        ),
        Transition(
            trigger="ship_order",
            source="Payment_Processed",
            dest="Shipped",
            before=["update_inventory"],
            after=["track_shipment", "send_notification"]
        ),
        Transition(
            trigger="deliver_order",
            source="Shipped",
            dest="Delivered",
            after=["update_status", "send_notification"]
        ),
        Transition(
            trigger="cancel_order",
            source="Order_Confirmed",
            dest="Cancelled",
            after=["refund_payment", "update_status", "send_notification"]
        ),
        Transition(
            trigger="return_order",
            source="Delivered",
            dest="Returned",
            conditions=["validate_input"],
            after=["initiate_return", "refund_payment", "update_status"]
        ),
    ],
    methods=[
        StateMethod(name="verify_data", body="Check if the order data is complete and valid."),
        StateMethod(name="send_notification", body="Send a notification to the customer about the current order status."),
        StateMethod(name="validate_input", body="Ensure all inputs are valid for processing."),
        StateMethod(name="check_compliance", body="Verify compliance with financial regulations."),
        StateMethod(name="generate_invoice", body="Create an invoice for the confirmed order."),
        StateMethod(name="send_receipt", body="Send a payment receipt to the customer."),
        StateMethod(name="update_inventory", body="Deduct the ordered items from inventory."),
        StateMethod(name="track_shipment", body="Initiate and track the shipment of the order."),
        StateMethod(name="update_status", body="Update the status of the order in the system."),
        StateMethod(name="refund_payment", body="Process the refund for the customer."),
        StateMethod(name="initiate_return", body="Handle the return process for returned orders.")
    ]
)

def main():
    """Main function"""

    # Example data
    # data = FSMClassModel(
    #     class_name="TrafficLight",
    #     states=["green", "yellow", "red"],
    #     transitions=[
    #         Transition(trigger="slow_down", source="green", dest="yellow"),
    #         Transition(trigger="stop", source="yellow", dest="red"),
    #         Transition(trigger="go", source="red", dest="green")
    #     ],
    #     methods=[
    #         StateMethod(name="log_transition", body='print("Logging transition.")'),
    #         StateMethod(name="celebrate_red", body='print("Celebrating red light!")')
    #     ]
    # )
    #
    from dspygen.modules.gen_pydantic_instance import instance
    # from dspygen.utils.dspy_tools import init_dspy
    # init_dspy(model="gpt-4")
    print("Generating data...")
    # data = instance(FSMClassModel, prompt)

    # print(data)
    data = revops_fsm

    from dspygen.typetemp.functional import render
    output = render(tmpl, to="{{ class_name | underscore }}.py",
                    class_name=data.class_name, states=data.states, transitions=data.transitions, methods=data.methods)
    print(output)


if __name__ == '__main__':
    main()
