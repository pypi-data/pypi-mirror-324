from abc import ABC, abstractmethod
from functools import lru_cache
from typing import Any, Dict, List, Optional, Text, Tuple, Union

import structlog
from jinja2 import Template

import rasa.shared.utils.io
from rasa.dialogue_understanding.commands import (
    Command,
)
from rasa.dialogue_understanding.generator import CommandGenerator
from rasa.dialogue_understanding.generator.constants import (
    DEFAULT_LLM_CONFIG,
    FLOW_RETRIEVAL_ACTIVE_KEY,
    FLOW_RETRIEVAL_FLOW_THRESHOLD,
    FLOW_RETRIEVAL_KEY,
    LLM_CONFIG_KEY,
)
from rasa.dialogue_understanding.generator.flow_retrieval import FlowRetrieval
from rasa.engine.graph import ExecutionContext, GraphComponent
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.shared.core.domain import Domain
from rasa.shared.core.flows import Flow, FlowsList, FlowStep
from rasa.shared.core.flows.steps.collect import CollectInformationFlowStep
from rasa.shared.core.trackers import DialogueStateTracker
from rasa.shared.exceptions import FileIOException, ProviderClientAPIException
from rasa.shared.nlu.constants import FLOWS_IN_PROMPT
from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.training_data.training_data import TrainingData
from rasa.shared.providers.llm.llm_response import LLMResponse
from rasa.shared.utils.health_check.llm_health_check_mixin import LLMHealthCheckMixin
from rasa.shared.utils.llm import (
    allowed_values_for_slot,
    llm_factory,
    resolve_model_client_config,
)
from rasa.utils.log_utils import log_llm

structlogger = structlog.get_logger()


@DefaultV1Recipe.register(
    [
        DefaultV1Recipe.ComponentType.COMMAND_GENERATOR,
    ],
    is_trainable=True,
)
class LLMBasedCommandGenerator(
    LLMHealthCheckMixin, GraphComponent, CommandGenerator, ABC
):
    """An abstract class defining interface and common functionality
    of an LLM-based command generators.
    """

    def __init__(
        self,
        config: Dict[str, Any],
        model_storage: ModelStorage,
        resource: Resource,
        **kwargs: Any,
    ) -> None:
        super().__init__(config)
        self.config = {**self.get_default_config(), **config}
        self.config[LLM_CONFIG_KEY] = resolve_model_client_config(
            self.config.get(LLM_CONFIG_KEY), LLMBasedCommandGenerator.__name__
        )
        self._model_storage = model_storage
        self._resource = resource
        self.flow_retrieval: Optional[FlowRetrieval]

        if self.enabled_flow_retrieval:
            self.flow_retrieval = FlowRetrieval(
                self.config[FLOW_RETRIEVAL_KEY], model_storage, resource
            )
            structlogger.info("llm_based_command_generator.flow_retrieval.enabled")
            self.config[FLOW_RETRIEVAL_KEY] = self.flow_retrieval.config
        else:
            self.flow_retrieval = None

    ### Abstract methods
    @staticmethod
    @abstractmethod
    def get_default_config() -> Dict[str, Any]:
        """The component's default config."""
        pass

    @classmethod
    @abstractmethod
    def load(
        cls: Any,
        config: Dict[str, Any],
        model_storage: ModelStorage,
        resource: Resource,
        execution_context: ExecutionContext,
        **kwargs: Any,
    ) -> "LLMBasedCommandGenerator":
        """Loads trained component (see parent class for full docstring)."""
        pass

    @abstractmethod
    def persist(self) -> None:
        """Persist the component to disk for future loading."""
        pass

    @abstractmethod
    async def predict_commands(
        self,
        message: Message,
        flows: FlowsList,
        tracker: Optional[DialogueStateTracker] = None,
        **kwargs: Any,
    ) -> List[Command]:
        """Predict commands using the LLM.

        Args:
            message: The message from the user.
            flows: The flows available to the user.
            tracker: The tracker containing the current state of the conversation.
            **kwargs: Keyword arguments for forward compatibility.

        Returns:
            The commands generated by the llm.
        """
        pass

    @abstractmethod
    def parse_commands(
        cls, actions: Optional[str], tracker: DialogueStateTracker, flows: FlowsList
    ) -> List[Command]:
        """Parse the actions returned by the llm into intent and entities.

        Args:
            actions: The actions returned by the llm.
            tracker: The tracker containing the current state of the conversation.
            flows: the list of flows

        Returns:
            The parsed commands.
        """
        pass

    @classmethod
    @abstractmethod
    def fingerprint_addon(cls: Any, config: Dict[str, Any]) -> Optional[str]:
        """Add a fingerprint of the knowledge base for the graph."""
        pass

    ### Shared implementations of GraphComponent parent
    @classmethod
    def create(
        cls,
        config: Dict[str, Any],
        model_storage: ModelStorage,
        resource: Resource,
        execution_context: ExecutionContext,
    ) -> "LLMBasedCommandGenerator":
        """Creates a new untrained component (see parent class for full docstring)."""
        return cls(config, model_storage, resource)

    def train(
        self, training_data: TrainingData, flows: FlowsList, domain: Domain
    ) -> Resource:
        """Train the llm based command generator. Stores all flows into a vector
        store.
        """
        self.perform_llm_health_check(
            self.config.get(LLM_CONFIG_KEY),
            DEFAULT_LLM_CONFIG,
            "llm_based_command_generator.train",
            LLMBasedCommandGenerator.__name__,
        )

        if (
            self.flow_retrieval is None
            and len(flows.user_flows) > FLOW_RETRIEVAL_FLOW_THRESHOLD
        ):
            structlogger.warn(
                "llm_based_command_generator.flow_retrieval.disabled",
                event_info=(
                    f"You have {len(flows.user_flows)} user flows but flow "
                    f"retrieval is disabled. "
                    f"It is recommended to enable flow retrieval if the "
                    f"total number of user flows exceed "
                    f"{FLOW_RETRIEVAL_FLOW_THRESHOLD}. "
                    f"Keeping it disabled can result in deterioration of "
                    f"command generator's functional "
                    f"performance and higher costs because of increased "
                    f"number of tokens in the prompt. For more"
                    "information see:\n"
                    "https://rasa.com/docs/rasa-pro/concepts/dialogue-understanding#how-the-llmcommandgenerator-works"
                ),
            )

        # flow retrieval is populated with only user-defined flows
        try:
            if self.flow_retrieval is not None and not flows.is_empty():
                self.flow_retrieval.populate(flows.user_flows, domain)
        except Exception as e:
            structlogger.error(
                "llm_based_command_generator.train.failed",
                event_info="Flow retrieval store is inaccessible.",
                error=e,
            )
            raise

        self.persist()
        return self._resource

    ### Helper methods
    @property
    def enabled_flow_retrieval(self) -> bool:
        return self.config[FLOW_RETRIEVAL_KEY].get(FLOW_RETRIEVAL_ACTIVE_KEY, True)

    @lru_cache
    def compile_template(self, template: str) -> Template:
        """Compile the prompt template.

        Compiling the template is an expensive operation,
        so we cache the result.
        """
        return Template(template)

    @classmethod
    def load_prompt_template_from_model_storage(
        cls,
        model_storage: ModelStorage,
        resource: Resource,
        prompt_template_file_name: str,
    ) -> Optional[Text]:
        try:
            with model_storage.read_from(resource) as path:
                return rasa.shared.utils.io.read_file(path / prompt_template_file_name)
        except (FileNotFoundError, FileIOException) as e:
            structlogger.warning(
                "llm_based_command_generator.load_prompt_template.failed",
                error=e,
                resource=resource.name,
            )
        return None

    @classmethod
    def load_flow_retrival(
        cls,
        config: Dict[str, Any],
        model_storage: ModelStorage,
        resource: Resource,
    ) -> Optional[FlowRetrieval]:
        """Load the FlowRetrieval component if it is enabled in the configuration."""
        enable_flow_retrieval = config.get(FLOW_RETRIEVAL_KEY, {}).get(
            FLOW_RETRIEVAL_ACTIVE_KEY, True
        )
        if enable_flow_retrieval:
            return FlowRetrieval.load(
                config=config.get(FLOW_RETRIEVAL_KEY),
                model_storage=model_storage,
                resource=resource,
            )
        return None

    async def filter_flows(
        self,
        message: Message,
        flows: FlowsList,
        tracker: Optional[DialogueStateTracker] = None,
    ) -> FlowsList:
        """Filters the available flows.

        Args:
            message: The message from the user.
            flows: The flows available to the user.
            tracker: The tracker containing the current state of the conversation.

        Returns:
            Filtered list of flows.
        """
        # If the flow retrieval is disabled, use the all the provided flows.
        filtered_flows = (
            await self.flow_retrieval.filter_flows(tracker, message, flows)
            if self.flow_retrieval is not None
            else flows
        )
        # Filter flows based on current context (tracker and message)
        # to identify which flows LLM can potentially start.
        if tracker:
            filtered_flows = tracker.get_startable_flows(filtered_flows)
        else:
            filtered_flows = filtered_flows

        # add the filtered flows to the message for evaluation purposes
        message.set(
            FLOWS_IN_PROMPT, list(filtered_flows.user_flow_ids), add_to_output=True
        )
        log_llm(
            logger=structlogger,
            log_module="LLMBasedCommandGenerator",
            log_event="llm_based_command_generator.predict_commands.filtered_flows",
            message=message.data,
            enabled_flow_retrieval=self.flow_retrieval is not None,
            relevant_flows=list(filtered_flows.user_flow_ids),
        )
        return filtered_flows

    async def invoke_llm(self, prompt: Text) -> Optional[LLMResponse]:
        """Use LLM to generate a response.

        Args:
            prompt: The prompt to send to the LLM.

        Returns:
            An LLMResponse object.

        Raises:
            ProviderClientAPIException: If an error occurs during the LLM API call.
        """
        llm = llm_factory(self.config.get(LLM_CONFIG_KEY), DEFAULT_LLM_CONFIG)
        try:
            return await llm.acompletion(prompt)
        except Exception as e:
            # unfortunately, langchain does not wrap LLM exceptions which means
            # we have to catch all exceptions here
            structlogger.error("llm_based_command_generator.llm.error", error=e)
            raise ProviderClientAPIException(
                message="LLM call exception", original_exception=e
            )

    def prepare_flows_for_template(
        self, flows: FlowsList, tracker: DialogueStateTracker
    ) -> List[Dict[str, Any]]:
        """Format data on available flows for insertion into the prompt template.

        Args:
            flows: The flows available to the user.
            tracker: The tracker containing the current state of the conversation.

        Returns:
            The inputs for the prompt template.
        """
        result = []
        for flow in flows.user_flows:
            slots_with_info = [
                {
                    "name": q.collect,
                    "description": q.description,
                    "allowed_values": allowed_values_for_slot(tracker.slots[q.collect]),
                }
                for q in flow.get_collect_steps()
                if self.is_extractable(q, tracker)
            ]
            result.append(
                {
                    "name": flow.id,
                    "description": flow.description,
                    "slots": slots_with_info,
                }
            )
        return result

    @staticmethod
    def is_extractable(
        collect_step: CollectInformationFlowStep,
        tracker: DialogueStateTracker,
        current_step: Optional[FlowStep] = None,
    ) -> bool:
        """Check if the `collect` can be filled.

        A collect slot can only be filled if the slot exist
        and either the collect has been asked already or the
        slot has been filled already.

        Args:
            collect_step: The collect_information step.
            tracker: The tracker containing the current state of the conversation.
            current_step: The current step in the flow.

        Returns:
            `True` if the slot can be filled, `False` otherwise.
        """
        slot = tracker.slots.get(collect_step.collect)
        if slot is None:
            return False

        return (
            # we can fill because this is a slot that can be filled ahead of time
            not collect_step.ask_before_filling
            # we can fill because the slot has been filled already
            or slot.has_been_set
            # we can fill because the is currently getting asked
            or (
                current_step is not None
                and isinstance(current_step, CollectInformationFlowStep)
                and current_step.collect == collect_step.collect
            )
        )

    @staticmethod
    def get_slot_value(tracker: DialogueStateTracker, slot_name: str) -> str:
        """Get the slot value from the tracker.

        Args:
            tracker: The tracker containing the current state of the conversation.
            slot_name: The name of the slot.

        Returns:
            The slot value as a string.
        """
        slot_value = tracker.get_slot(slot_name)
        if slot_value is None:
            return "undefined"
        else:
            return str(slot_value)

    def prepare_current_flow_slots_for_template(
        self, top_flow: Flow, current_step: FlowStep, tracker: DialogueStateTracker
    ) -> List[Dict[str, Any]]:
        """Prepare the current flow slots for the template.

        Args:
            top_flow: The top flow.
            current_step: The current step in the flow.
            tracker: The tracker containing the current state of the conversation.

        Returns:
            The slots with values, types, allowed values and a description.
        """
        if top_flow is not None:
            flow_slots = [
                {
                    "name": collect_step.collect,
                    "value": self.get_slot_value(tracker, collect_step.collect),
                    "type": tracker.slots[collect_step.collect].type_name,
                    "allowed_values": allowed_values_for_slot(
                        tracker.slots[collect_step.collect]
                    ),
                    "description": collect_step.description,
                }
                for collect_step in top_flow.get_collect_steps()
                if self.is_extractable(collect_step, tracker, current_step)
            ]
        else:
            flow_slots = []
        return flow_slots

    def prepare_current_slot_for_template(
        self, current_step: FlowStep
    ) -> Tuple[Union[str, None], Union[str, None]]:
        """Prepare the current slot for the template."""
        return (
            (current_step.collect, current_step.description)
            if isinstance(current_step, CollectInformationFlowStep)
            else (None, None)
        )
