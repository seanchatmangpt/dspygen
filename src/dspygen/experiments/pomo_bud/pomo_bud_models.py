from typing import List, Dict, Any, Optional, Union
from pydantic import BaseModel, Field, validator

from dspygen.utils.yaml_tools import YAMLMixin


class FeatureSpecification(BaseModel):
    """
    Describes the specifications for each feature, including inputs, outputs, and configuration parameters.
    """
    feature_name: str = Field(..., description="Unique name of the feature.")
    inputs: List[str] = Field(default=[], description="List of expected inputs.")
    outputs: List[str] = Field(default=[], description="List of possible outputs.")
    configurations: Dict[str, Any] = Field(default={}, description="Configuration parameters for the feature.")


class SensoryCapability(FeatureSpecification):
    """
    Enhanced sensory input model capturing detailed specifications for processing various sensory data.
    """
    sensory_type: str = Field(..., description="Type of sensory data to be processed.")


class ActuatorCapability(FeatureSpecification):
    """
    Detailed actuator model defining the actions that can be performed in the physical or digital world.
    """
    actuator_type: str = Field(..., description="Type of action the actuator performs.")


class CognitiveFunction(FeatureSpecification):
    """
    Represents a cognitive function or model with enhanced capabilities for decision making and processing.
    """
    cognitive_type: str = Field(..., description="Type of cognitive processing or decision-making model.")


class LearningMechanism(FeatureSpecification):
    """
    Defines learning mechanisms with parameters for how the system can learn or adapt over time.
    """
    learning_type: str = Field(..., description="Type of learning mechanism.")


class InteractionProtocol(FeatureSpecification):
    """
    Specifies the protocols for human-AI interaction, including conversational interfaces.
    """
    protocol_type: str = Field(..., description="Type of interaction protocol, e.g., conversational AI, gestures.")


class ContinuousAdaptationMechanism(BaseModel):
    """
    Mechanisms for continuous learning and self-adaptation, with validators ensuring correct configuration.
    """
    mechanism_name: str = Field(..., description="Name of the adaptation mechanism.")
    details: Dict[str, Any] = Field(..., description="Detailed configuration for the adaptation mechanism.")


class AGISystemConfiguration(BaseModel, YAMLMixin):
    """
    Top-level model defining an AGI system's configuration using the DSL, capable of migrating existing conversational systems.
    """
    system_name: str = Field(..., description="Name of the AGI system.")
    sensory_capabilities: List[SensoryCapability] = Field(default=[], description="Sensory processing capabilities.")
    actuators: List[ActuatorCapability] = Field(default=[], description="Actuator capabilities.")
    cognitive_functions: List[CognitiveFunction] = Field(default=[], description="Cognitive processing functions.")
    learning_mechanisms: List[LearningMechanism] = Field(default=[], description="Learning and adaptation mechanisms.")
    interaction_protocols: List[InteractionProtocol] = Field(default=[], description="Human-AI interaction protocols.")
    continuous_adaptation: List[ContinuousAdaptationMechanism] = Field(default=[],
                                                                       description="Mechanisms for continuous system adaptation.")


def main2():
    """Main function"""
    # Example configuration for a system with basic conversational capabilities, learning, and sensory processing
    example_agi_system = AGISystemConfiguration(
        system_name="OSIRIS-PomoBud",
        sensory_capabilities=[
            SensoryCapability(feature_name="SpeechRecognition", sensory_type="Auditory", inputs=["audio"],
                              outputs=["text"]),
        ],
        actuators=[
            ActuatorCapability(feature_name="TextToSpeech", actuator_type="Speech", inputs=["text"], outputs=["audio"]),
        ],
        cognitive_functions=[
            CognitiveFunction(feature_name="NaturalLanguageUnderstanding", cognitive_type="NLP", inputs=["text"],
                              outputs=["intent", "entities"]),
        ],
        learning_mechanisms=[
            LearningMechanism(feature_name="ReinforcementLearning", learning_type="Adaptive",
                              configurations={"learning_rate": 0.01}),
        ],
        interaction_protocols=[
            InteractionProtocol(feature_name="ConversationalInterface", protocol_type="ConversationalAI",
                                inputs=["text"], outputs=["response"]),
        ],
        continuous_adaptation=[
            ContinuousAdaptationMechanism(mechanism_name="SelfModification", details={"update_frequency": "weekly"}),
        ]
    )

    print(example_agi_system)


def main():
    inst = AGISystemConfiguration.from_yaml("pomo_bud_dsl.yaml")
    print(inst)


if __name__ == '__main__':
    main()
