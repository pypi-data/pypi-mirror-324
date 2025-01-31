from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Literal, Self, cast

from google.protobuf import timestamp_pb2, struct_pb2

from .protobufs.clavata.gateway.v1 import jobs_pb2
from .protobufs.clavata.shared.v1 import shared_pb2

from google.protobuf.message import Message

type JsonAny = dict[str, "JsonAny"] | list["JsonAny"] | str | int | float | bool | None
type OutcomeName = Literal["TRUE", "FALSE", "FAILED"]
type JobStatusName = Literal["PENDING", "RUNNING", "COMPLETED", "FAILED", "CANCELED"]


def to_proto_timestamp(dt: datetime) -> timestamp_pb2.Timestamp:
    return timestamp_pb2.Timestamp(
        seconds=int(dt.timestamp()),
        nanos=int((dt.timestamp() - int(dt.timestamp())) * 1e9),
    )


def from_proto_job_status(
    status: shared_pb2.JobStatus,
) -> JobStatusName:
    match status:
        case shared_pb2.JOB_STATUS_PENDING:
            return "PENDING"
        case shared_pb2.JOB_STATUS_RUNNING:
            return "RUNNING"
        case shared_pb2.JOB_STATUS_COMPLETED:
            return "COMPLETED"
        case shared_pb2.JOB_STATUS_FAILED:
            return "FAILED"
        case shared_pb2.JOB_STATUS_CANCELED:
            return "CANCELED"
        case _:
            raise ValueError(f"Unknown or unspecified job status: {status}")


def to_proto_job_status(status: JobStatusName) -> shared_pb2.JobStatus:
    match status:
        case "PENDING":
            return shared_pb2.JOB_STATUS_PENDING
        case "RUNNING":
            return shared_pb2.JOB_STATUS_RUNNING
        case "COMPLETED":
            return shared_pb2.JOB_STATUS_COMPLETED
        case "FAILED":
            return shared_pb2.JOB_STATUS_FAILED
        case "CANCELED":
            return shared_pb2.JOB_STATUS_CANCELED
        case _:
            raise ValueError(f"Unknown or unspecified job status: {status}")


def from_proto_outcome(outcome: shared_pb2.Outcome) -> OutcomeName:
    match outcome:
        case shared_pb2.OUTCOME_TRUE:
            return "TRUE"
        case shared_pb2.OUTCOME_FALSE:
            return "FALSE"
        case shared_pb2.OUTCOME_FAILED:
            return "FAILED"
        case _:
            raise ValueError(f"Unknown or unspecified outcome: {outcome}")


def to_structpb_value(value: JsonAny) -> struct_pb2.Value:
    if isinstance(value, dict):
        return struct_pb2.Value(
            struct_value=struct_pb2.Struct(
                fields={k: to_structpb_value(v) for k, v in value.items()}
            )
        )
    if isinstance(value, list):
        return struct_pb2.Value(
            list_value=struct_pb2.ListValue(values=[to_structpb_value(v) for v in value])
        )
    if isinstance(value, str):
        return struct_pb2.Value(string_value=str(value))
    if isinstance(value, bool):
        return struct_pb2.Value(bool_value=value)
    if isinstance(value, (int, float)):
        return struct_pb2.Value(number_value=value)

    return struct_pb2.Value(null_value=struct_pb2.NULL_VALUE)


class BaseModel(ABC):
    @abstractmethod
    def to_proto(self) -> Message:
        pass

    @classmethod
    @abstractmethod
    def from_proto(cls, proto: Message) -> Self:
        pass


@dataclass
class ContentData(BaseModel):
    """
    Used to send the request data for the create_job and evaluate methods.

    ### Fields:
    - text: The text content to evaluate.
    - image: The image content to evaluate.

    #### Note:
    At present, either text or image must be provided. Not both. In the future, we will likely
    add support for both types to be included if they are logically related.
    """

    text: str | None = None
    image: bytes | None = None

    def to_proto(self) -> shared_pb2.ContentData:
        return shared_pb2.ContentData(
            text=self.text,
            image=self.image,
        )

    @staticmethod
    def from_proto(proto: shared_pb2.ContentData) -> "ContentData":
        return ContentData(
            text=proto.text,
            image=proto.image,
        )


@dataclass
class CreateJobRequest(BaseModel):
    """
    Used to send the request data for the create_job method.

    ### Fields:
    - content: The content to evaluate. Can be either a single ContentData object or a list of ContentData objects.
    If a single ContentData object is provided, it will be automatically converted to a list. Alternatively, you
    may provide a string, in which case it will be assumed the content is text and a single ContentData object
    will be created with the provided string.
    - policy_id: The ID of the policy to use for content evaluation.
    - wait_for_completion: If True, the request will wait for the job to complete before returning.
    If False, the request will return immediately after the job is created and you can then use a
    GetJobRequest to check the status of the job. If a job is complete, the results will be returned
    in the response.
    """

    content: list[ContentData] | ContentData | str
    policy_id: str
    wait_for_completion: bool

    def __post_init__(self):
        # Ensure that we convert a single ContentData object to a list so we can be confident that it is always a list
        if isinstance(self.content, ContentData):
            self.content = [self.content]
        elif isinstance(self.content, str):
            self.content = [ContentData(text=self.content)]

    @classmethod
    def from_proto(cls, proto: jobs_pb2.CreateJobRequest) -> "CreateJobRequest":
        return cls(
            content=[ContentData.from_proto(content) for content in proto.content_data],
            policy_id=proto.policy_id,
            wait_for_completion=proto.wait_for_completion,
        )

    def to_proto(self) -> jobs_pb2.CreateJobRequest:
        return jobs_pb2.CreateJobRequest(
            content_data=[content.to_proto() for content in cast(list[ContentData], self.content)],
            policy_id=self.policy_id,
            wait_for_completion=self.wait_for_completion,
        )


@dataclass
class SectionEvaluationReport(BaseModel):
    name: str
    message: str
    result: OutcomeName

    def to_proto(self) -> shared_pb2.PolicyEvaluationReport.SectionEvaluationReport:
        return shared_pb2.PolicyEvaluationReport.SectionEvaluationReport(
            name=self.name,
            message=self.message,
            result=self.result,
        )

    @classmethod
    def from_proto(
        cls,
        proto: shared_pb2.PolicyEvaluationReport.SectionEvaluationReport,
    ) -> "SectionEvaluationReport":
        return cls(
            name=proto.name,
            message=proto.message,
            result=from_proto_outcome(proto.result),
        )


@dataclass
class PolicyEvaluationReport[T: JsonAny](BaseModel):
    policy_id: str
    policy_name: str
    policy_version_id: str
    result: OutcomeName
    section_evaluation_reports: list[SectionEvaluationReport]
    content_hash: str
    content_metadata: T

    def to_proto(self) -> shared_pb2.PolicyEvaluationReport:
        struct_pb2.Value()
        return shared_pb2.PolicyEvaluationReport(
            policy_id=self.policy_id,
            policy_key=self.policy_name,
            policy_version_id=self.policy_version_id,
            result=self.result,
            section_evaluation_reports=[
                section.to_proto() for section in self.section_evaluation_reports
            ],
            content_hash=self.content_hash,
            content_metadata=to_structpb_value(self.content_metadata),
        )

    @staticmethod
    def from_proto(proto: shared_pb2.PolicyEvaluationReport) -> "PolicyEvaluationReport":
        return PolicyEvaluationReport(
            policy_id=proto.policy_id,
            policy_name=proto.policy_key,
            policy_version_id=proto.policy_version_id,
            result=from_proto_outcome(proto.result),
            section_evaluation_reports=[
                SectionEvaluationReport.from_proto(section)
                for section in proto.section_evaluation_reports
            ],
            content_hash=proto.content_hash,
            content_metadata=cast(T, proto.content_metadata),
        )


@dataclass
class JobResult(BaseModel):
    uuid: str
    job_uuid: str
    content_hash: str
    report: PolicyEvaluationReport
    created: datetime

    def to_proto(self) -> shared_pb2.JobResult:
        return shared_pb2.JobResult(
            uuid=self.uuid,
            job_uuid=self.job_uuid,
            content_hash=self.content_hash,
            report=self.report.to_proto(),
            created=to_proto_timestamp(self.created),
        )

    @staticmethod
    def from_proto(proto: shared_pb2.JobResult) -> "JobResult":
        return JobResult(
            uuid=proto.uuid,
            job_uuid=proto.job_uuid,
            content_hash=proto.content_hash,
            report=PolicyEvaluationReport.from_proto(proto.report),
            created=proto.created.ToDatetime(),
        )


@dataclass
class Job(BaseModel):
    job_uuid: str
    customer_id: str
    policy_id: str
    policy_version_id: str
    status: JobStatusName
    content_data: list[ContentData]
    results: list[JobResult]
    created: datetime
    updated: datetime
    completed: datetime

    def to_proto(self) -> shared_pb2.Job:
        return shared_pb2.Job(
            job_uuid=self.job_uuid,
            customer_id=self.customer_id,
            policy_id=self.policy_id,
            policy_version_id=self.policy_version_id,
            status=to_proto_job_status(self.status),
            content_data=[content.to_proto() for content in self.content_data],
            results=[result.to_proto() for result in self.results],
            created=to_proto_timestamp(self.created),
            updated=to_proto_timestamp(self.updated),
            completed=to_proto_timestamp(self.completed),
        )

    @classmethod
    def from_proto(cls, proto: shared_pb2.Job) -> "Job":
        return Job(
            job_uuid=proto.job_uuid,
            customer_id=proto.customer_id,
            policy_id=proto.policy_id,
            policy_version_id=proto.policy_version_id,
            status=from_proto_job_status(proto.status),
            content_data=[ContentData.from_proto(content) for content in proto.content_data],
            results=[JobResult.from_proto(result) for result in proto.results],
            created=proto.created.ToDatetime(),
            updated=proto.updated.ToDatetime(),
            completed=proto.completed.ToDatetime(),
        )


@dataclass
class CreateJobResponse(Job):
    def to_proto(self) -> jobs_pb2.CreateJobResponse:
        return jobs_pb2.CreateJobResponse(job=super().to_proto())

    @classmethod
    def from_proto(cls, proto: jobs_pb2.CreateJobResponse) -> "CreateJobResponse":
        job = super().from_proto(proto.job)
        return CreateJobResponse(**job.__dict__)


@dataclass
class EvaluateRequest(BaseModel):
    """
    Used to send the request data for the evaluate method.

    ### Fields:
    - content: The content to evaluate. Can be either a single ContentData object or a list of ContentData objects.
    If a single ContentData object is provided, it will be automatically converted to a list.
    - policy_id: The ID of the policy to evaluate the content against.
    - include_evaluation_report: Whether to include the full evaluation report in the response. If False, only the result for
    the entire policy is returned
    """

    content: list[ContentData] | ContentData | str
    policy_id: str
    include_evaluation_report: bool

    def __post_init__(self):
        # Ensure that we convert a single ContentData object to a list so we can be confident that it is always a list
        if isinstance(self.content, ContentData):
            self.content = [self.content]
        elif isinstance(self.content, str):
            self.content = [ContentData(text=self.content)]

    @classmethod
    def from_proto(cls, proto: jobs_pb2.EvaluateRequest) -> "EvaluateRequest":
        return cls(
            content=[ContentData.from_proto(content) for content in proto.content_data],
            policy_id=proto.policy_id,
            include_evaluation_report=proto.include_evaluation_report,
        )

    def to_proto(self) -> jobs_pb2.EvaluateRequest:
        return jobs_pb2.EvaluateRequest(
            content_data=[content.to_proto() for content in cast(list[ContentData], self.content)],
            policy_id=self.policy_id,
            include_evaluation_report=self.include_evaluation_report,
        )


@dataclass
class EvaluateResponse(BaseModel):
    job_uuid: str
    content_hash: str
    policy_evaluation_report: PolicyEvaluationReport

    def to_proto(self) -> jobs_pb2.EvaluateResponse:
        return jobs_pb2.EvaluateResponse(
            job_uuid=self.job_uuid,
            content_hash=self.content_hash,
            policy_evaluation_report=self.policy_evaluation_report.to_proto(),
        )

    @staticmethod
    def from_proto(proto: jobs_pb2.EvaluateResponse) -> "EvaluateResponse":
        return EvaluateResponse(
            job_uuid=proto.job_uuid,
            content_hash=proto.content_hash,
            policy_evaluation_report=PolicyEvaluationReport.from_proto(
                proto.policy_evaluation_report
            ),
        )


@dataclass
class EvaluateOneRequest(BaseModel):
    content: ContentData | str
    policy_id: str
    wait_for_completion: bool

    def __post_init__(self):
        if isinstance(self.content, str):
            self.content = ContentData(text=self.content)

    def to_proto(self) -> jobs_pb2.CreateJobRequest:
        return jobs_pb2.CreateJobRequest(
            content_data=[cast(ContentData, self.content).to_proto()],
            policy_id=self.policy_id,
            wait_for_completion=self.wait_for_completion,
        )

    @classmethod
    def from_proto(cls, proto: jobs_pb2.CreateJobRequest) -> "EvaluateOneRequest":
        raise NotImplementedError("EvaluateOneRequest is not implemented")


@dataclass
class EvaluateOneResponse(BaseModel):
    job_uuid: str
    content_hash: str
    report: PolicyEvaluationReport
    status: JobStatusName

    def to_proto(self) -> jobs_pb2.CreateJobResponse:
        raise NotImplementedError("EvaluateOneResponse is not implemented")

    @classmethod
    def from_proto(cls, proto: jobs_pb2.CreateJobResponse) -> "EvaluateOneResponse":
        # Get the one result to work from
        result = proto.job.results[0]
        return cls(
            job_uuid=proto.job.job_uuid,
            content_hash=result.content_hash,
            report=PolicyEvaluationReport.from_proto(result.report),
            status=from_proto_job_status(proto.job.status),
        )


@dataclass
class TimeRange(BaseModel):
    start: datetime
    end: datetime
    inclusive: bool

    def to_proto(self) -> shared_pb2.TimeRange:
        return shared_pb2.TimeRange(
            start=to_proto_timestamp(self.start),
            end=to_proto_timestamp(self.end),
            inclusive=self.inclusive,
        )

    @classmethod
    def from_proto(cls, proto: shared_pb2.TimeRange) -> "TimeRange":
        return TimeRange(
            start=proto.start.ToDatetime(),
            end=proto.end.ToDatetime(),
            inclusive=proto.inclusive,
        )


@dataclass
class ListJobsQuery(BaseModel):
    created_time_range: TimeRange
    updated_time_range: TimeRange
    completed_time_range: TimeRange
    status: JobStatusName

    def to_proto(self) -> jobs_pb2.ListJobsRequest.Query:
        return jobs_pb2.ListJobsRequest.Query(
            created_time_range=self.created_time_range.to_proto(),
            updated_time_range=self.updated_time_range.to_proto(),
            completed_time_range=self.completed_time_range.to_proto(),
            status=to_proto_job_status(self.status),
        )

    def to_proto_request(self) -> jobs_pb2.ListJobsRequest:
        return jobs_pb2.ListJobsRequest(query=self.to_proto())

    @classmethod
    def from_proto(cls, proto: jobs_pb2.ListJobsRequest.Query) -> "ListJobsQuery":
        return cls(
            created_time_range=TimeRange.from_proto(proto.created_time_range),
            updated_time_range=TimeRange.from_proto(proto.updated_time_range),
            completed_time_range=TimeRange.from_proto(proto.completed_time_range),
            status=from_proto_job_status(proto.status),
        )


@dataclass
class ListJobsResponse(BaseModel):
    jobs: list[Job]

    def to_proto(self) -> jobs_pb2.ListJobsResponse:
        return jobs_pb2.ListJobsResponse(jobs=[job.to_proto() for job in self.jobs])

    @classmethod
    def from_proto(cls, proto: jobs_pb2.ListJobsResponse) -> "ListJobsResponse":
        return ListJobsResponse(jobs=[Job.from_proto(job) for job in proto.jobs])


@dataclass
class GetJobRequest(BaseModel):
    job_uuid: str

    def to_proto(self) -> jobs_pb2.GetJobRequest:
        return jobs_pb2.GetJobRequest(job_uuid=self.job_uuid)

    @classmethod
    def from_proto(cls, proto: jobs_pb2.GetJobRequest) -> "GetJobRequest":
        return cls(job_uuid=proto.job_uuid)


@dataclass
class GetJobResponse(Job):
    def to_proto(self) -> jobs_pb2.GetJobResponse:
        return jobs_pb2.GetJobResponse(job=super().to_proto())

    @classmethod
    def from_proto(cls, proto: jobs_pb2.GetJobResponse) -> "GetJobResponse":
        job = super().from_proto(proto.job)
        return GetJobResponse(**job.__dict__)
