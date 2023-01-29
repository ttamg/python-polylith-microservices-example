[back to intro](README.md)

# Testing microservices

Testing of asynchronous microservices has tended to be a bit of a pain to set up and do in Python. The fact taht they are asynchronous means that they are not easy to test in the same way as synchronous code.

In the past I have needed to build a mock for the RabbitMQ queue and also for the database so as to run unit tests.

Integration tests are then important to ensure the microservices talk together but this has been difficult to automate with the existing python tools.

I am hoping that the Polylith framework can help make this a bit easier to set up and maintain ...

NOT YET COMPLETED
