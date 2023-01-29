[back to intro](README.md)

# Creating our first asynchronous worker

Now we have created one component already, we will follow the same process to build the other components and bases required for our asynchronous workers.

## RabbitMQ setup

Before we dive in, we need to decide on a message queue to use. For this tutorial we will use RabbitMQ.

To keep it close to how it would be deployed, we will spin up a RabbitMQ container using docker that will be used on my local machine for development.

The following docker-compose [`development.yml`](deploy/development.yml) file will spin up a RabbitMQ instance with some simple username and password for development purposes.

```yaml
# deploy/development.yml

version: "3.4"

services:
  rabbit:
    image: rabbitmq:management
    restart: always
    ports:
      - 5672:5672
      - 15672:15672
    environment:
      RABBITMQ_DEFAULT_USER: DEV_USER
      RABBITMQ_DEFAULT_PASS: CHANGE_ME
    logging:
      driver: local
```

> Note that the Polylith framework seems to be silent on where to put docker-compose files and similar orchestration and script files. I've made the decision to put such things in a `deploy` folder on the workspace.
>
> The docker-compose files don't really fit within the `projects` folder concept as they are not about building deployable artifacts, but more about how to spin up and orchestrate them.

We can spin up our RabbitMQ instance using

    docker-compose -f deploy/development.yml up

Or if we want it to remain up in the background

      docker-compose -f deploy/development.yml up -d

We can check that RabbitMQ is up and running by checking the management app on http://localhost:15672

---

## Our first worker

Our first worker will do the following:

- Connects to the job queue
- Listens for new jobs on the job queue (which will later be triggered from the API)
- Fetches data when triggered - this will be the component we aready created to simulate reading an external API
- Pushes that fetched data to another job queue for the next worker to pick up
- Then it sits and waits for the next job

One of the good things about the bricks structure in the Polylith architecture is that it forces us to think about our structure up front. This worker can be set up as three different bricks:

1. We have already built one **component** brick to simulate fetching the data from an external api in the last step
2. We can build a **base** brick that makes a connection with the RabbitMQ job queue. This is going to be something that all the workers and API will need so let's carve this out into one brick.
3. The logic that this particular worker uses to when a job is posted for it can be set up as another **component**

We can go ahead and create the two missing bricks now using the poetry poly CLI

      poetry poly create base --name job_queue
      poetry poly create component --name run_fetch_worker

## Prototyping in development folder

Again we can use our `development` folder to do some fast prototyping. The messaging in these sort of Consumer-Producer asynchronous systems can be a bit fiddly to get right, so it's a good idea to prototype in a notebook first.

My first attempt is a [simple notebook](development/02_queue_worker.ipynb) that creates a producer and a worker and shows that they can communicate. It also shows that the RabbitMQ container is working and able to be connected with.

This can now be refactored into the bricks we want. Again doing this in a notebook makes for a fast development process. The [refactored notebook](development/03_queue_worker_refactoring.ipynb) shows the main pieces of logic we will use in our bricks.

## The job_queue base

This **base** craates a connection to RabbitMQ and will be used by all the workers and the API.

From the prototyping notebook [refactored notebook](development/03_queue_worker_refactoring.ipynb) we can drop in the code very quickly.

```python
# bases/mousetrap/job_queue/core.py

import os
import pika

QUEUES = ["start_fetch", "data_processing"]

username = os.environ.get("RABBITMQ_USER", "DEV_USER")
password = os.environ.get("RABBITMQ_PASSWORD", "CHANGE_ME")
host = os.environ.get("RABBITMQ_HOST", "localhost")


def open_channel():
    """
    Opens a connection, a channel, creates queues and then returns this to the caller.
    """

    # Create the connection
    credentials = pika.PlainCredentials(username, password)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=host, credentials=credentials)
    )
    channel = connection.channel()

    # Create all the queues
    for queue in QUEUES:
        channel.queue_declare(queue=queue, durable=True)

    return channel
```

All we want to explose is the `open_channel()` function so that other components can call it and get a connection to the job queue. As before we do this be defining this **interface** in the `__init__.py` file

```python
# bases/mousetrap/job_queue/__init__.py

from mousetrap.job_queue.core import open_channel

__all__ = ["open_channel"]
```

Again we also register this in the development `pyproject.toml` file in the root.

## The run_fetch_worker component

Similarly we can create this worker from the same refactored prototypes.

Note that this uses the connection and also the data simulation so we have an import from the `job_queue` base and from the `fetch_data` component.

```python
# components/mousetrap/run_fetch_worker/core.py

import json

from mousetrap.fetch_data import fetch_data
from mousetrap.job_queue import open_channel

LISTEN_QUEUE = "start_fetch"
PUSH_QUEUE = "data_processing"


def callback(ch, method, properties, body):
    """
    Fetches data and hands it off to the next queue.
    """

    print("Fetch data job started...")

    # Fall the fetch data component to create and fetch data
    data = fetch_data()

    # Send data to the next queue
    ch.basic_publish(exchange="", routing_key=PUSH_QUEUE, body=json.dumps(data))

    # Acknowledge the incoming message to remove it from the queue
    ch.basic_ack(delivery_tag=method.delivery_tag)

    print("Done. Data sent to to queue for data processing.")


def run_fetch_worker():
    """
    Sets up and runs the fetch worker 1.
    Creates a blocking connection so remains running.
    """

    # Get a new channel from the base
    channel = open_channel()

    # Register the callback
    channel.basic_consume(queue=LISTEN_QUEUE, on_message_callback=callback)

    # This is a blocking connection
    channel.start_consuming()
```

> Note that the imports of other bricks uses the Polylith workspace namespace and then the brick name. This is not a full path import.
>
> This is important because when the application is built, the imports will be from the 'compiled' package in Poetry so that will be `mousetrap.component_name`. That is what will be used and where we import from.

---

We have all the bricks we need defined for the first worker (the data fetch worker). Next we can code up the other workers in a similar way.

[next](TUTORIAL_3B.md)
