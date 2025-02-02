import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    KeysView,
    List,
    Literal,
    Optional,
    TypeVar,
    Union,
)

from .evaluator import EvaluatorType

Input = Literal["INPUT"]
ExpectedOutput = Literal["EXPECTED_OUTPUT"]
ContextToEvaluate = Literal["CONTEXT_TO_EVALUATE"]
Variable = Literal["VARIABLE"]
NullableVariable = Literal["NULLABLE_VARIABLE"]
Output = Literal["OUTPUT"]

DataStructure = Dict[
    str, Union[Input, ExpectedOutput, ContextToEvaluate, Variable, NullableVariable]
]

T = TypeVar("T", bound=DataStructure)


class CSVFile:
    def __init__(self, file_path: str, column_mapping: Dict[str, int]):
        self.file_path = file_path
        self.column_mapping = column_mapping


DataValue = List[T]


@dataclass
class YieldedOutputTokenUsage:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    latency: Optional[float]

    def to_dict(self):
        return {
            "promptTokens": self.prompt_tokens,
            "completionTokens": self.completion_tokens,
            "totalTokens": self.total_tokens,
            "latency": self.latency,
        }


@dataclass
class YieldedOutputCost:
    input_cost: float
    output_cost: float
    total_cost: float

    def to_dict(self):
        return {
            "input": self.input_cost,
            "output": self.output_cost,
            "total": self.total_cost,
        }


@dataclass
class YieldedOutputMeta:
    usage: Optional[YieldedOutputTokenUsage] = None
    cost: Optional[YieldedOutputCost] = None

    def __json__(self):
        return {
            "usage": self.usage.__json__() if self.usage else None,
            "cost": self.cost.__json__() if self.cost else None,
        }

    def to_dict(self):
        return {
            "usage": self.usage.to_dict() if self.usage else None,
            "cost": self.cost.to_dict() if self.cost else None,
        }

    @classmethod
    def from_json(cls, json_str: str):
        data = json.loads(json_str)
        return cls(
            usage=(
                YieldedOutputTokenUsage(**data["usage"]) if data.get("usage") else None
            ),
            cost=YieldedOutputCost(**data["cost"]) if data.get("cost") else None,
        )

    @classmethod
    def dict_to_class(cls, data: Dict[str, Any]):
        return cls(
            usage=YieldedOutputTokenUsage(data["usage"]) if data.get("usage") else None,
            cost=YieldedOutputCost(data["cost"]) if data.get("cost") else None,
        )


@dataclass
class YieldedOutput:
    data: str
    retrieved_context_to_evaluate: Optional[List[str]] = None
    meta: Optional[YieldedOutputMeta] = None


@dataclass
class EvaluatorArgs:
    output: str
    input: Optional[str] = None
    expectedOutput: Optional[str] = None
    contextToEvaluate: Optional[Union[str, List[str]]] = None


@dataclass
class PlatformEvaluatorType(Generic[T]):
    type: Literal["platform"]
    name: str
    mappingOverrides: Optional[
        Dict[str, Union[str, KeysView[T]]] if T else Dict[str, str]
    ] = None


@dataclass
class HumanEvaluationConfig:
    emails: List[str]
    instructions: Optional[str] = None
    requester: Optional[str] = None

    def __json__(self):
        return {
            "emails": self.emails,
            "instructions": self.instructions,
            "requester": self.requester,
        }

    def to_dict(self):
        return {
            k: v
            for k, v in {
                "emails": self.emails,
                "instructions": self.instructions,
                "requester": self.requester,
            }.items()
            if v is not None
        }


@dataclass
class RunType(Enum):
    SINGLE = "SINGLE"
    COMPARISON = "COMPARISON"

    def __json__(self):
        return self.value

    @classmethod
    def from_string(cls, value: str) -> "RunType":
        try:
            return cls(value)
        except ValueError:
            raise ValueError(f"Invalid RunType: {value}")


@dataclass
class EvaluatorConfig:
    id: str
    name: str
    type: EvaluatorType
    builtin: bool
    reversed: Optional[bool] = False

    def __json__(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type.value,
            "builtin": self.builtin,
            "reversed": self.reversed,
        }

    def to_dict(self):
        return {
            k: v
            for k, v in {
                "id": self.id,
                "name": self.name,
                "type": self.type.value,
                "builtin": self.builtin,
                "reversed": self.reversed,
            }.items()
            if v is not None
        }


@dataclass
class TestRun:
    id: str
    workspace_id: str
    eval_config: Dict[str, Any]
    human_evaluation_config: Optional[HumanEvaluationConfig] = None
    parent_test_run_id: Optional[str] = None

    def to_dict(self):
        return {
            k: v
            for k, v in {
                "id": self.id,
                "workspaceId": self.workspace_id,
                "evalConfig": self.eval_config,
                "humanEvaluationConfig": (
                    self.human_evaluation_config.to_dict()
                    if self.human_evaluation_config
                    else None
                ),
                "parentTestRunId": self.parent_test_run_id,
            }.items()
            if v is not None
        }

    def __json__(self):
        return {
            "id": self.id,
            "workspaceId": self.workspace_id,
            "evalConfig": self.eval_config,
            "humanEvaluationConfig": (
                self.human_evaluation_config.__json__()
                if self.human_evaluation_config
                else None
            ),
            "parentTestRunId": self.parent_test_run_id,
        }

    @classmethod
    def from_json(cls, json_str: str):
        data = json.loads(json_str)
        return cls(
            id=data["id"],
            workspace_id=data["workspaceId"],
            eval_config=data["evalConfig"],
            human_evaluation_config=(
                HumanEvaluationConfig(**data["humanEvaluationConfig"])
                if data.get("humanEvaluationConfig")
                else None
            ),
            parent_test_run_id=data.get("parentTestRunId"),
        )

    @classmethod
    def dict_to_class(cls, data: Dict[str, Any]) -> "TestRun":
        return cls(
            id=data["id"],
            workspace_id=data["workspaceId"],
            eval_config=data["evalConfig"],
            human_evaluation_config=(
                HumanEvaluationConfig(data["humanEvaluationConfig"])
                if data.get("humanEvaluationConfig")
                else None
            ),
            parent_test_run_id=data.get("parentTestRunId"),
        )


@dataclass
class TestRunEntry:
    output: str
    input: Optional[str] = None
    expected_output: Optional[str] = None
    context_to_evaluate: Optional[Union[str, List[str]]] = None

    def to_dict(self):
        result = {}
        if self.output is not None:
            result["output"] = self.output
        if self.input is not None:
            result["input"] = self.input
        if self.expected_output is not None:
            result["expectedOutput"] = self.expected_output
        if self.context_to_evaluate is not None:
            result["contextToEvaluate"] = self.context_to_evaluate
        return result

    def __json__(self):
        return {
            key: value
            for key, value in {
                "output": self.output,
                "input": self.input,
                "expectedOutput": self.expected_output,
                "contextToEvaluate": self.context_to_evaluate,
            }.items()
            if value is not None
        }

    @classmethod
    def from_json(cls, json_str: str):
        data = json.loads(json_str)
        return cls(
            output=data["output"],
            input=data.get("input"),
            expected_output=data.get("expectedOutput"),
            context_to_evaluate=data.get("contextToEvaluate"),
        )

    @classmethod
    def dict_to_class(cls, data: Dict[str, Any]):
        return cls(
            output=data["output"],
            input=data.get("input"),
            expected_output=data.get("expectedOutput"),
            context_to_evaluate=data.get("contextToEvaluate"),
        )


@dataclass
class TestRunWithDatasetEntry(TestRun):

    def __init__(self, test_run: TestRun, dataset_entry_id: str, dataset_id: str):
        super().__init__(
            id=test_run.id,
            workspace_id=test_run.workspace_id,
            eval_config=test_run.eval_config,
            human_evaluation_config=test_run.human_evaluation_config,
            parent_test_run_id=test_run.parent_test_run_id,
        )
        self.dataset_entry_id = dataset_entry_id
        self.dataset_id = dataset_id

    def __json__(self):
        base_json = super().__json__()
        base_json.update(
            {
                "datasetEntryId": self.dataset_entry_id,
                "datasetId": self.dataset_id,
            }
        )
        return base_json

    def to_dict(self):
        return {
            k: v
            for k, v in {
                "datasetEntryId": self.dataset_entry_id,
                "datasetId": self.dataset_id,
                "id": self.id,
                "workspaceId": self.workspace_id,
                "evalConfig": self.eval_config,
                "humanEvaluationConfig": (
                    self.human_evaluation_config.__json__()
                    if self.human_evaluation_config
                    else None
                ),
                "parentTestRunId": self.parent_test_run_id,
            }.items()
            if v is not None
        }

    @classmethod
    def from_json(cls, json_str: str):
        data = json.loads(json_str)
        return cls(**cls.dict_to_class(data))

    @classmethod
    def dict_to_class(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        base_dict = super().dict_to_class(data)
        base_dict.update(
            {
                "dataset_entry_id": data["datasetEntryId"],
                "dataset_id": data["datasetId"],
            }
        )
        return base_dict


@dataclass
class RunStatus(Enum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    FAILED = "FAILED"
    COMPLETE = "COMPLETE"
    STOPPED = "STOPPED"


@dataclass
class TestRunStatus:
    total_entries: int
    running_entries: int
    queued_entries: int
    failed_entries: int
    completed_entries: int
    stopped_entries: int
    test_run_status: RunStatus

    def to_dict(self):
        return {
            "totalEntries": self.total_entries,
            "runningEntries": self.running_entries,
            "queuedEntries": self.queued_entries,
            "failedEntries": self.failed_entries,
            "completedEntries": self.completed_entries,
            "stoppedEntries": self.stopped_entries,
            "testRunStatus": self.test_run_status.value,
        }

    @classmethod
    def from_json(cls, json_str: str) -> "TestRunStatus":
        data = json.loads(json_str)
        return cls(**cls.dict_to_class(data))

    @classmethod
    def dict_to_class(cls, data: Dict[str, Any]) -> "TestRunStatus":
        return cls(
            total_entries=data["total"],
            running_entries=data["running"],
            queued_entries=data["queued"],
            failed_entries=data["failed"],
            completed_entries=data["completed"],
            stopped_entries=data["stopped"],
            test_run_status=RunStatus(data["testRunStatus"]),
        )


@dataclass
class EvaluatorMeanScore:
    score: Union[float, bool, str]
    out_of: Optional[float] = None
    is_pass: Optional[bool] = None

    def __json__(self):
        return {"score": self.score, "outOf": self.out_of, "pass": self.is_pass}

    @classmethod
    def from_json(cls, json_str: str) -> "EvaluatorMeanScore":
        data = json.loads(json_str)
        return cls(**cls.dict_to_class(data))

    @classmethod
    def dict_to_class(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        return cls(
            score=data["score"], out_of=data.get("outOf"), is_pass=data.get("pass")
        )


@dataclass
class TestRunTokenUsage:
    total: int
    input: int
    completion: int

    def __json__(self):
        return {
            "total": self.total,
            "input": self.input,
            "completion": self.completion,
        }

    @classmethod
    def from_json(cls, json_str: str) -> "TestRunTokenUsage":
        data = json.loads(json_str)
        return cls(**cls.dict_to_class(data))

    @classmethod
    def dict_to_class(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        return cls(
            total=data["total"],
            input=data["input"],
            completion=data["completion"],
        )


@dataclass
class TestRunCost:
    total: float
    input: float
    completion: float

    def __json__(self):
        return {
            "total": self.total,
            "input": self.input,
            "completion": self.completion,
        }

    @classmethod
    def from_json(cls, json_str: str) -> "TestRunCost":
        data = json.loads(json_str)
        return cls(**cls.dict_to_class(data))

    @classmethod
    def dict_to_class(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        return cls(
            total=data["total"],
            input=data["input"],
            completion=data["completion"],
        )


@dataclass
class TestRunLatency:
    min: float
    max: float
    p50: float
    p90: float
    p95: float
    p99: float
    mean: float
    standard_deviation: float
    total: float

    def __json__(self):
        return {
            "min": self.min,
            "max": self.max,
            "p50": self.p50,
            "p90": self.p90,
            "p95": self.p95,
            "p99": self.p99,
            "mean": self.mean,
            "standardDeviation": self.standard_deviation,
            "total": self.total,
        }

    @classmethod
    def from_json(cls, json_str: str) -> "TestRunLatency":
        data = json.loads(json_str)
        return cls(**cls.dict_to_class(data))

    @classmethod
    def dict_to_class(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "min": data["min"],
            "max": data["max"],
            "p50": data["p50"],
            "p90": data["p90"],
            "p95": data["p95"],
            "p99": data["p99"],
            "mean": data["mean"],
            "standard_deviation": data["standardDeviation"],
            "total": data["total"],
        }


@dataclass
class TestRunResultObj:
    name: str
    individual_evaluator_mean_score: Dict[str, EvaluatorMeanScore]
    usage: Optional[TestRunTokenUsage] = None
    cost: Optional[TestRunCost] = None
    latency: Optional[TestRunLatency] = None

    def __json__(self):
        return {
            "name": self.name,
            "individualEvaluatorMeanScore": {
                k: v.__json__() for k, v in self.individual_evaluator_mean_score.items()
            },
            "usage": self.usage.__json__() if self.usage else None,
            "cost": self.cost.__json__() if self.cost else None,
            "latency": self.latency.__json__() if self.latency else None,
        }

    @classmethod
    def from_json(cls, json_str: str) -> "TestRunResultObj":
        data = json.loads(json_str)
        return cls(**cls.dict_to_class(data))

    @classmethod
    def dict_to_class(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        return cls(
            name=data["name"],
            individual_evaluator_mean_score={
                k: EvaluatorMeanScore.dict_to_class(v)
                for k, v in data["individualEvaluatorMeanScore"].items()
            },
            usage=(
                TestRunTokenUsage.dict_to_class(data["usage"])
                if data.get("usage")
                else None
            ),
            cost=(
                TestRunCost.dict_to_class(data["cost"]) if data.get("cost") else None
            ),
            latency=(
                TestRunLatency.dict_to_class(data["latency"])
                if data.get("latency")
                else None
            ),
        )


@dataclass
class TestRunResult:
    link: str
    result: List[TestRunResultObj]

    def __json__(self):
        return {"link": self.link, "result": [r.__json__() for r in self.result]}

    @classmethod
    def from_json(cls, json_str: str) -> "TestRunResult":
        data = json.loads(json_str)
        return cls(
            link=data["link"],
            result=[TestRunResultObj.from_json(json.dumps(r)) for r in data["result"]],
        )

    @classmethod
    def dict_to_class(cls, data: Dict[str, Any]) -> "TestRunResult":
        return cls(
            link=data["link"],
            result=[TestRunResultObj.dict_to_class(r) for r in data["result"]],
        )


@dataclass
class RunResult:
    test_run_result: TestRunResult
    failed_entry_indices: List[int]


class TestRunLogger(ABC):
    @abstractmethod
    def info(self, message: str) -> None:
        """
        Log an informational message.

        Args:
            message (str): The message to be logged.
        """
        pass

    @abstractmethod
    def error(self, message: str, e: Optional[Exception]) -> None:
        """
        Log an error message.

        Args:
            message (str): The error message to be logged.
        """
        pass


class ConsoleLogger(TestRunLogger):
    def info(self, message: str) -> None:
        print(message)

    def error(self, message: str, e: Optional[Exception]) -> None:
        print(message, e)


@dataclass
class TestRunConfig:
    base_url: str
    api_key: str
    in_workspace_id: str
    name: str
    data_structure: Optional[T] = None
    data: Optional[str or DataValue[T]] or Callable[[int], Optional[[DataValue[T]]]] = (
        None
    )
    test_config_id: Optional[str] = None
    platform_evaluators: List[PlatformEvaluatorType[T]] = None
    logger: Optional[TestRunLogger] = ConsoleLogger()
    human_evaluation_config: Optional[HumanEvaluationConfig] = None
    output_function: Optional[
        Callable[[DataValue[T]], Union[YieldedOutput, YieldedOutput]]
    ] = None
    concurrency: Optional[int] = None
