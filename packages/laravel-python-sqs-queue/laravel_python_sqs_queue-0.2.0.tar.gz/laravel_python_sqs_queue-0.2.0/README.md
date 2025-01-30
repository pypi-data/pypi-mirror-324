# Laravel Python SQS Queue

A Python package for creating and dispatching Laravel queue jobs to AWS SQS. This package allows Python applications to seamlessly integrate with Laravel's queue system by generating compatible job payloads.

## Features

- Create Laravel-compatible job payloads from Python
- Dispatch jobs directly to AWS SQS queues
- Support for job options like max tries, timeout, backoff, and tags
- Builder pattern for easy job configuration
- LocalStack support for development
- Comprehensive test coverage

## Installation

```bash
pip install laravel-python-sqs-queue
```

## Requirements

- Python 3.8+
- phpserialize>=1.3
- boto3>=1.26.0

## Quick Start

```python
from laravel_queue import LaravelJob

# Create and configure a job
job = (LaravelJob("App\\Jobs\\ExampleJob", {
        "message": "Hello from Python",
        "data": {
            "user_id": 123,
            "action": "test"
        }
    })
    .set_max_tries(3)
    .set_timeout(60)
    .add_tags("example", "test")
)

# Dispatch to SQS
response = job.dispatch_to_sqs(
    queue_url="YOUR_SQS_QUEUE_URL",
    aws_region="your-region"
)
```

## Detailed Usage

### Creating a Job

The `LaravelJob` class uses a builder pattern for configuration:

```python
from laravel_queue import LaravelJob
from datetime import datetime, timezone

job = (LaravelJob("App\\Jobs\\UserJob", {
        "user_id": 123,
        "action": "process"
    })
    .set_max_tries(3)           # Maximum number of retry attempts
    .set_timeout(60)            # Job timeout in seconds
    .set_backoff(5)            # Delay between retry attempts
    .set_delay(10)             # Initial delay before processing
    .set_retry_until(datetime.now(timezone.utc))  # Retry until timestamp
    .add_tags("user", "process")  # Add tags for tracking
    .add_middleware("custom-middleware")  # Add Laravel middleware
)
```

### Dispatching to SQS

```python
# Basic dispatch
response = job.dispatch_to_sqs(
    queue_url="https://sqs.us-east-1.amazonaws.com/123456789012/my-queue",  # Replace with your actual queue URL
    aws_region="us-east-1"
)

# With custom endpoint (e.g., LocalStack)
response = job.dispatch_to_sqs(
    queue_url="http://localhost:4566/000000000000/default",
    aws_region="ap-northeast-1",
    endpoint_url="http://localhost:4566"
)

# With explicit credentials
response = job.dispatch_to_sqs(
    queue_url="https://sqs.us-east-1.amazonaws.com/123456789012/my-queue",  # Replace with your actual queue URL
    aws_region="us-east-1",
    aws_access_key_id="your-key",
    aws_secret_access_key="your-secret"
)
```

### Legacy Functions

For backward compatibility, the package also provides standalone functions:

```python
from laravel_queue import create_laravel_job_payload, push_laravel_job_to_sqs

# Create payload only
payload = create_laravel_job_payload(
    "App\\Jobs\\ExampleJob",
    {"message": "test"}
)

# Create and dispatch
response = push_laravel_job_to_sqs(
    "your-queue-url",
    "App\\Jobs\\ExampleJob",
    {"message": "test"},
    aws_region="your-region"
)
```

## Development

### Setup

1. Clone the repository:
```bash
git clone https://github.com/nguyenkhactien/laravel-python-sqs-queue.git
cd laravel-python-sqs-queue
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

### Running Tests

The package includes comprehensive tests using pytest. For local testing, you'll need LocalStack running:

1. Start LocalStack (requires Docker):
```bash
docker run --rm -p 4566:4566 localstack/localstack
```

2. Run tests:
```bash
pytest
```

### Type Checking

```bash
mypy src/laravel_queue
```

### Code Formatting

```bash
black src/laravel_queue tests
isort src/laravel_queue tests
```

## Testing with Laravel

### Laravel Job Classes

To test the integration, you can use these sample Laravel job classes:

#### ExampleJob

```php
<?php

namespace App\Jobs;

use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;
use Illuminate\Support\Facades\Log;

class ExampleJob implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public string $message;
    public array $data;

    /**
     * Create a new job instance.
     */
    public function __construct(string $message, array $data)
    {
        $this->message = $message;
        $this->data = $data;
    }

    /**
     * Execute the job.
     */
    public function handle(): void
    {
        Log::info('Message from Python: ' . $this->message);
        Log::info('Data from Python:', $this->data);

        if (isset($this->data['user_id'])) {
            Log::info('Processing for user: ' . $this->data['user_id']);
        }

        if (isset($this->data['action'])) {
            Log::info('Action to perform: ' . $this->data['action']);
        }
    }
}
```

#### TestJob

```php
<?php

namespace App\Jobs;

use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;
use Illuminate\Support\Facades\Log;

class TestJob implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public string $message;
    public int $user_id;

    /**
     * Create a new job instance.
     */
    public function __construct(string $message, int $user_id)
    {
        $this->message = $message;
        $this->user_id = $user_id;
    }

    /**
     * Execute the job.
     */
    public function handle(): void
    {
        Log::info('Processing TestJob', [
            'message' => $this->message,
            'user_id' => $this->user_id
        ]);
    }
}
```

### Testing Integration

1. Place these job classes in your Laravel project under `app/Jobs/`.

2. From Python, you can dispatch jobs that match these classes:

```python
# Testing ExampleJob
job = (LaravelJob("App\\Jobs\\ExampleJob", {
        "message": "Hello from Python",
        "data": {
            "user_id": 123,
            "action": "test"
        }
    })
    .set_max_tries(3)
    .set_timeout(60)
)

# Testing TestJob
job = (LaravelJob("App\\Jobs\\TestJob", {
        "message": "Test message",
        "user_id": 123
    })
    .set_max_tries(3)
    .set_timeout(60)
)
```

3. Check Laravel logs to verify job execution:
```bash
tail -f storage/logs/laravel.log
```

You should see log entries from the jobs showing the data passed from Python.

### LocalStack Testing

For local development, you can use LocalStack to simulate AWS SQS:

1. Start LocalStack:
```bash
docker run --rm -p 4566:4566 localstack/localstack
```

2. Update your Laravel `.env`:
```
QUEUE_CONNECTION=sqs
AWS_ACCESS_KEY_ID=test
AWS_SECRET_ACCESS_KEY=test
AWS_DEFAULT_REGION=ap-northeast-1
SQS_LOCALSTACK_URL=http://localstack:4566
SQS_PREFIX=http://localstack:4566/000000000000
SQS_QUEUE=default
```

3. Update your `config\queue.php`:
```
'sqs' => [
    ...
    'endpoint' => env('SQS_LOCALSTACK_URL'),
],
```

3. Run Laravel queue worker:
```bash
php artisan queue:work sqs
```

4. Dispatch jobs from Python using LocalStack endpoint:
```python
response = job.dispatch_to_sqs(
    queue_url="http://localhost:4566/000000000000/default",
    aws_region="ap-northeast-1",
    endpoint_url="http://localhost:4566",
    aws_access_key_id="test",
    aws_secret_access_key="test"
)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.