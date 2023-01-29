# job_queue

This base creates a connection to a job queue which in production will be a RabbitMQ container.

This component exposes a channel object that can be used to connect with.

We will also make sure all the valid queues are created by this base on the RabbitMQ instance.
