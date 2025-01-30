import pytest
import json
import time
from datetime import datetime, timedelta, timezone
from unittest.mock import Mock, patch
from laravel_queue import LaravelJob, LaravelQueueException

@pytest.fixture
def sample_job_data():
    return {
        "message": "Test message",
        "user_id": 123
    }

@pytest.fixture
def sample_job_class():
    return "App\\Jobs\\TestJob"

def test_basic_job_creation(sample_job_class, sample_job_data):
    job = LaravelJob(sample_job_class, sample_job_data)
    payload = json.loads(job.get_payload())
    
    assert payload["displayName"] == sample_job_class
    assert "uuid" in payload
    assert payload["job"] == "Illuminate\\Queue\\CallQueuedHandler@call"

def test_job_with_all_options(sample_job_class, sample_job_data):
    now = datetime.now(timezone.utc)
    job = (LaravelJob(sample_job_class, sample_job_data)
           .set_max_tries(3)
           .set_timeout(60)
           .set_backoff(5)
           .set_delay(10)
           .set_retry_until(now)
           .add_tags("tag1", "tag2")
           .add_middleware("middleware1"))
    
    payload = json.loads(job.get_payload())
    
    assert payload["maxTries"] == 3
    assert payload["timeout"] == 60
    assert payload["backoff"] == 5
    assert payload["delay"] == 10
    assert payload["retryUntil"] == int(now.timestamp())
    assert payload["tags"] == ["tag1", "tag2"]
    assert payload["middleware"] == ["middleware1"]

@patch('boto3.client')
def test_dispatch_to_sqs(mock_boto3_client, sample_job_class, sample_job_data):
    mock_sqs = Mock()
    mock_boto3_client.return_value = mock_sqs
    mock_sqs.send_message.return_value = {"MessageId": "test-message-id"}
    
    job = LaravelJob(sample_job_class, sample_job_data)
    response = job.dispatch_to_sqs(
        queue_url="https://sqs.test-region.amazonaws.com/test-queue",
        aws_region="test-region"
    )
    
    assert response["MessageId"] == "test-message-id"
    mock_sqs.send_message.assert_called_once()

def test_invalid_job_data():
    with pytest.raises(LaravelQueueException):
        job = LaravelJob("InvalidJob", {"invalid": object()})
        job.get_payload()
