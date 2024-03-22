from dspy import Signature, InputField, OutputField, ChainOfThought, Module, Prediction
import dspy



# Define Signature Classes for SEBLG Components
class CaptureRequirementsSignature(Signature):
    input_description = InputField(desc="Description of the system's requirements and existing business logic.")
    event_storming_output = OutputField(
        prefix="```python",
        desc="Reqs converted to python code")


class SelfEvolvingLogicSignature(Signature):
    event_storming_results = InputField(desc="EventStorming results identifying key domains and processes.")
    updated_logic = OutputField(desc="Automatically updated business logic reflecting new requirements or changes.")


class DecentralizedUpdatesSignature(Signature):
    updated_logic = InputField(desc="Updated business logic ready for dissemination.")
    dissemination_result = OutputField(desc="Confirmation of successful logic updates across the system.")


class SEBLGFinalOutcomeSignature(Signature):
    updated_logic = InputField(desc="The evolved business logic after adaptation.")
    dissemination_result = InputField(desc="The result of disseminating the evolved logic across the system.")
    final_outcome = OutputField(
        desc="Confirmation of successful adaptation and dissemination, along with any relevant details.")


# Implement the SEBLGPipeline Module
class SEBLGPipeline(Module):
    def __init__(self):
        super().__init__()
        self.capture_requirements = ChainOfThought(CaptureRequirementsSignature)
        self.self_evolving_logic = ChainOfThought(SelfEvolvingLogicSignature)
        self.decentralized_updates = ChainOfThought(DecentralizedUpdatesSignature)
        self.final_outcome = ChainOfThought(SEBLGFinalOutcomeSignature)  # New ChainOfThought for final outcome

    def forward(self, system_description, iterations=3):
        current_description = system_description
        for _ in range(iterations):  # Loop to simulate continuous evolution
            event_storming_results = self.capture_requirements(
                input_description=current_description).event_storming_output
            print(f"{event_storming_results=}")
            updated_logic = self.self_evolving_logic(event_storming_results=event_storming_results).updated_logic
            print(f"{updated_logic=}")
            dissemination_result = self.decentralized_updates(updated_logic=updated_logic).dissemination_result
            print(f"{dissemination_result=}")
            current_description = updated_logic  # Update the current description for the next iteration
            print(f"{current_description=}")

        # Final outcome step, summarizing the adaptation and dissemination results
        final_result = self.final_outcome(updated_logic=updated_logic,
                                          dissemination_result=dissemination_result).final_outcome

        return Prediction(final_outcome=final_result)

    def __call__(self, system_description, iterations=3):
        return self.forward(system_description=system_description, iterations=iterations)


bpmn = """bpmn:
  - process:
      id: "ups_tracking_and_label_printing"
      name: "UPS Tracking and Label Printing Process"
      tasks:
        - id: "start"
          name: "Start"
          type: "startEvent"
        - id: "track_shipment"
          name: "Track Shipment"
          type: "serviceTask"
          properties:
            service: "UPS Tracking API"
        - id: "decision_tree"
          name: "Decision Tree Analysis"
          type: "exclusiveGateway"
          properties:
            decisionLogic: "Determine next steps based on tracking status"
        - id: "print_label"
          name: "Print Label"
          type: "serviceTask"
          properties:
            service: "Label Printing Service"
        - id: "web_browser_automation"
          name: "Automate Web Browser"
          type: "serviceTask"
          properties:
            service: "Web Browser Automation Tool"
        - id: "end"
          name: "End"
          type: "endEvent"
      flows:
        - id: "flow1"
          sourceRef: "start"
          targetRef: "track_shipment"
        - id: "flow2"
          sourceRef: "track_shipment"
          targetRef: "decision_tree"
        - id: "flow3"
          sourceRef: "decision_tree"
          targetRef: "print_label"
          condition: "status == 'Delivered'"
        - id: "flow4"
          sourceRef: "decision_tree"
          targetRef: "web_browser_automation"
          condition: "status != 'Delivered'"
        - id: "flow5"
          sourceRef: "print_label"
          targetRef: "end"
        - id: "flow6"
          sourceRef: "web_browser_automation"
          targetRef: "end"
"""

cmmn = """cmmn:
  case:
    id: "ups_tracking_and_handling"
    name: "UPS Tracking and Handling Case"
    roles:
      - id: "user"
        name: "User"
      - id: "system"
        name: "System"
    stages:
      - id: "tracking_stage"
        name: "Tracking Stage"
        tasks:
          - id: "track_shipment"
            name: "Track Shipment"
            type: "humanTask"
            role: "system"
            description: "Track the shipment using UPS Tracking API."
      - id: "decision_making_stage"
        name: "Decision Making Stage"
        tasks:
          - id: "analyze_status"
            name: "Analyze Shipment Status"
            type: "humanTask"
            role: "system"
            description: "Analyze the status of the shipment to determine next actions."
    planItems:
      - id: "print_label_task"
        name: "Print Label Task"
        type: "humanTask"
        role: "system"
        description: "Print the shipping label if the package is delivered."
        entryCriterion: "shipment_delivered"
      - id: "automate_browser_task"
        name: "Automate Browser Task"
        type: "humanTask"
        role: "system"
        description: "Automate browser tasks for further actions if the package is not delivered."
        entryCriterion: "shipment_not_delivered"
    sentries:
      - id: "shipment_delivered"
        name: "Shipment Delivered"
        condition: "Shipment status is 'Delivered'"
      - id: "shipment_not_delivered"
        name: "Shipment Not Delivered"
        condition: "Shipment status is not 'Delivered'"
"""

dmn = """dmn:
  definitions:
    id: "shipment_decision_logic"
    name: "Shipment Decision Logic"
    decision:
      - id: "decision_1"
        name: "Determine Action Based on Shipment Status"
        decisionTable:
          inputs:
            - id: "input_1"
              label: "Shipment Status"
              inputExpression: "status"
              inputValues: ["Delivered", "In Transit", "Exception"]
          outputs:
            - id: "output_1"
              label: "Action"
              outputValues: ["Print Label", "Automate Browser", "Notify User"]
          rules:
            - inputEntries:
                - "Delivered"
              outputEntries:
                - "Print Label"
            - inputEntries:
                - "In Transit"
              outputEntries:
                - "Automate Browser"
            - inputEntries:
                - "Exception"
              outputEntries:
                - "Notify User"
"""

def main():
    from dspygen.utils.dspy_tools import init_dspy
    init_dspy()

    seblg_pipeline = SEBLGPipeline()
    system_description = f"{bpmn}\n{cmmn}\n{dmn}"
    result = seblg_pipeline(system_description, iterations=5)
    print(result.final_outcome)


if __name__ == '__main__':
    main()
