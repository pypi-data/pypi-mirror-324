import pytest
import boto3
import json
from datetime import datetime, UTC
from laravel_queue import LaravelJob
from . import TEST_ENDPOINT, TEST_REGION, TEST_QUEUE_URL

@pytest.fixture
def sqs_client():
    """Create SQS client for testing"""
    return boto3.client('sqs',
                       endpoint_url=TEST_ENDPOINT,
                       region_name=TEST_REGION,
                       aws_access_key_id='test',
                       aws_secret_access_key='test')

def test_localstack_integration(sqs_client):
    """
    Test with LocalStack using default queue and ap-northeast-1 region
    Required: LocalStack running on port 4566
    """
    # Create default queue
    try:
        sqs_client.create_queue(QueueName='default')
    except Exception as e:
        print(f"Queue might already exist: {e}")
    
    # Create job payload matching Laravel TestJob
    job = (LaravelJob("App\\Jobs\\TestJob", {
            "message": "Test from Python",
            "user_id": 123
        })
        .set_max_tries(3)
        .set_timeout(60)
        .add_tags("test", "python")
    )
    
    # Dispatch to SQS
    response = job.dispatch_to_sqs(
        queue_url=TEST_QUEUE_URL,
        aws_region=TEST_REGION,
        endpoint_url=TEST_ENDPOINT
    )
    
    assert response.get('MessageId') is not None
    print(f"\nJob dispatched successfully with MessageId: {response['MessageId']}")
    
    # Read message from queue
    messages = sqs_client.receive_message(
        QueueUrl=TEST_QUEUE_URL,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=1
    )
    
    assert 'Messages' in messages
    message = json.loads(messages['Messages'][0]['Body'])
    print("\nReceived message from queue:")
    print(json.dumps(message, indent=2))
    
    # Verify message structure
    assert message['displayName'] == "App\\Jobs\\TestJob"
    assert message['maxTries'] == 3
    assert message['tags'] == ["test", "python"]
    assert 'data' in message
    assert 'command' in message['data']

def test_job_payload_matches_laravel_job():
    """Test that generated payload matches Laravel TestJob structure"""
    job = LaravelJob("App\\Jobs\\TestJob", {
        "message": "Test message",
        "user_id": 123
    })
    
    payload = json.loads(job.get_payload())
    
    # Verify required fields
    assert payload['displayName'] == "App\\Jobs\\TestJob"
    assert payload['job'] == "Illuminate\\Queue\\CallQueuedHandler@call"
    assert 'uuid' in payload
    assert 'data' in payload
    assert 'command' in payload['data']
    assert payload['data']['commandName'] == "App\\Jobs\\TestJob"