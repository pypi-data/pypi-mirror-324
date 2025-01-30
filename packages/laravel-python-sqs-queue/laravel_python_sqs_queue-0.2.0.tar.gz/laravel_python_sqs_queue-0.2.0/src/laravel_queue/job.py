import uuid
import json
import time
import phpserialize
import boto3
from typing import Optional, Dict, Any, Union
from datetime import datetime, timezone
from .exceptions import LaravelQueueException

class LaravelJob:
    """Class representing a Laravel Job with builder pattern"""

    def __init__(
        self,
        job_class: str,
        job_data: Dict[str, Any],
        queue: Optional[str] = None
    ):
        self.job_class = job_class
        self.job_data = job_data
        self.queue = queue
        self.max_tries = None
        self.max_exceptions = None
        self.fail_on_timeout = False
        self.backoff = None
        self.timeout = None
        self.retry_until = None
        self.delay = None
        self.middleware = []
        self.tags = []
        self._queue_handler = "Illuminate\\Queue\\CallQueuedHandler@call"

    def set_max_tries(self, tries: int) -> 'LaravelJob':
        self.max_tries = tries
        return self

    def set_max_exceptions(self, exceptions: int) -> 'LaravelJob':
        self.max_exceptions = exceptions
        return self

    def set_timeout(self, seconds: int) -> 'LaravelJob':
        self.timeout = seconds
        return self

    def set_retry_until(self, timestamp: Union[int, datetime]) -> 'LaravelJob':
        if isinstance(timestamp, datetime):
            self.retry_until = int(timestamp.timestamp())
        else:
            self.retry_until = timestamp
        return self

    def set_backoff(self, seconds: int) -> 'LaravelJob':
        self.backoff = seconds
        return self

    def set_delay(self, seconds: int) -> 'LaravelJob':
        self.delay = seconds
        return self

    def add_tags(self, *tags: str) -> 'LaravelJob':
        self.tags.extend(tags)
        return self

    def add_middleware(self, *middleware: str) -> 'LaravelJob':
        self.middleware.extend(middleware)
        return self

    def get_payload(self) -> str:
        """Generate Laravel job payload"""
        try:
            obj = phpserialize.phpobject(
                self.job_class.encode('utf-8'),
                {
                    key.encode('utf-8'): (
                        value.encode('utf-8') if isinstance(value, str) else value
                    )
                    for key, value in self.job_data.items()
                }
            )
            serialized_obj = phpserialize.dumps(obj).decode('utf-8')

            payload = {
                "uuid": str(uuid.uuid4()),
                "displayName": self.job_class,
                "job": self._queue_handler,
                "maxTries": self.max_tries,
                "maxExceptions": self.max_exceptions,
                "failOnTimeout": self.fail_on_timeout,
                "backoff": self.backoff,
                "timeout": self.timeout,
                "retryUntil": self.retry_until,
                "data": {
                    "commandName": self.job_class,
                    "command": serialized_obj
                },
                "tags": self.tags,
                "middleware": self.middleware,
            }

            if self.queue:
                payload["queue"] = self.queue

            if self.delay:
                payload["delay"] = self.delay

            return json.dumps(payload)
        except Exception as e:
            raise LaravelQueueException(f"Failed to create job payload: {str(e)}")

    def dispatch_to_sqs(
        self,
        queue_url: str,
        aws_region: str = "us-east-1",
        endpoint_url: Optional[str] = None,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """Dispatch job to SQS queue"""
        try:
            sqs_client = boto3.client(
                'sqs',
                region_name=aws_region,
                endpoint_url=endpoint_url,
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key
            )

            message_params = {
                'QueueUrl': queue_url,
                'MessageBody': self.get_payload()
            }

            if self.delay:
                message_params['DelaySeconds'] = min(self.delay, 900)  # SQS max delay is 15 minutes

            return sqs_client.send_message(**message_params)
        except Exception as e:
            raise LaravelQueueException(f"Failed to push job to SQS: {str(e)}")

# Maintain backward compatibility
def create_laravel_job_payload(
    job_class: str,
    job_data: Dict[str, Any],
    **kwargs
) -> str:
    job = LaravelJob(job_class, job_data)
    for key, value in kwargs.items():
        if hasattr(job, key):
            setattr(job, key, value)
    return job.get_payload()

def push_laravel_job_to_sqs(
    queue_url: str,
    job_class: str,
    job_data: Dict[str, Any],
    aws_region: str = "us-east-1",
    endpoint_url: Optional[str] = None,
    **kwargs
) -> Dict[str, Any]:
    job = LaravelJob(job_class, job_data)
    for key, value in kwargs.items():
        if hasattr(job, key):
            setattr(job, key, value)
    return job.dispatch_to_sqs(queue_url, aws_region, endpoint_url)