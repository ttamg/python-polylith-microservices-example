[back to intro](README.md)

# Creating the other workers

We can now create the components needed for the other workers in a similar way.

## The start_fetch_worker component

We will need the API to be able to send a message to the job queue to start the first work. This is a very simple process of:

- Creating a connection to the job queue
- Sending a message to the queue to start a new fetch
- Closing down the connection

We can create this component the usual way

    poetry poly create component --name start_fetch_worker

This is also created the usual way as can be seen in the codebase example:

- [core.py](components/mousetrap/start_fetch_worker/core.py)
- [**init**.py](components/mousetrap/start_fetch_worker/__init__.py)

---

## MongoDB database

The second worker needs to store some data in a database. The API will also refer to it also. We will use MongoDB for this. We will spin it up as a service using docker-compose.

See the [deploy/development.yml](deploy/development.yml) file for the full docker-compose code including both RabbitMQ and MongoDB.

We will use the same approach as we did for RabbitMQ and create a base brick that creates a connection to MongoDB.

Create a base for MongoDB connection

    poetry poly create component --name mongo_connection

We also need to install the `pymongo` library

    poetry add pymongo

The code for the base brick is in [core.py](bases/mousetrap/mongo_connection/core.py)

---

## The second worker

This worker performs data processing on the data fetched by the first worker. It will do the following steps:

- Listen for a new job to process data
- Take the fetched data from the job queue and process it - we will simulate creating a summary of the data
- Pushing the summary to the MongoDB database
- Sitting and waiting for the next job to arrive

This worker can be turned into a number of bricks:

- A **base** brick called `mongo_connetion` that creates a connection to the MongoDB database.
  - See [core.py](bases/mousetrap/mongo_connection/core.py)
- A **component** called `process_data` that will take the fetched data and proicess it into a new method.
  - To prototype this, we created a notebook called [04_data_processing.ipynb](development/04_data_processing.ipynb)
  - It was then refactored into a component [core.py](components/mousetrap/process_data/core.py)
- A **component** called `run_processing_worker` that will run the worker and the interfacing with the job queue.
  - See component[core.py](components/mousetrap/run_processing_worker/core.py)

---

This gives us all the components for the workers. Next we can build the API using FastAPI.

[next](TUTORIAL_4.md)
