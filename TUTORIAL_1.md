[back to intro](README.md)

# Getting started and setup

This section of the tutorial deals with setup of the project and structure for a Python Polylith project.

## Polylith

We will use the [Polylith architecture](https://polylith.gitbook.io/polylith/introduction/polylith-in-a-nutshell) and Python tooling for it to test how how well the Polylith methods and tools work in a microservices use case.

## Monorepo and poetry setup

Create a new empty directory and repo for this project

    git init

Install Poetry if not already installed - I used homebrew on Mac to install Poetry

Add the basic poetry setup and follow the instructions

    poetry init

Add the poetry polylith and multiproject plugins that will allow us to set up and manage the Polylith setup using poetry

    poetry self add poetry-multiproject-plugin
    poetry self add poetry-polylith-plugin

Configure Poetry to create virtual environments in a local `.venv` folder

    poetry config virtualenvs.in-project true

## Install project dependencies

For my project I know I am going to need `fastapi` for the api, and `pika` for the message queues for this demo. I will also use `faker` to create dummy data.

Install the dependencies using

    poetry add fastapi uvicorn pika faker

Also install the development dependencies you want for your setup. For my setup I like the following with VSCode:

    poetry add --dev pylint isort pytest black ipykernel

## Create our workspace

Polylith has a specific directory structure that separates out the components, bases, projects and development. This is set up in what they call a **workspace**. The details can be read about in the [Polylith documentation](https://polylith.gitbook.io/polylith/architecture/2.1.-workspace).

David Vujic has reinterpreted these rules in the Python setting which is called the **loose theme**. This uses a directory structure that is more Pythonic and natural to Python devs. This tutorial will follow his suggestions and use this loose theme.

We use poetry with the poly plugin to set up our workspace and directory structure. I will give this project a name `mousetrap`

    poetry poly create workspace --name mousetrap --theme loose

This creates a `workspace.toml` file and also the directories for components, bases, projects and development.

---

We are now ready to start writing some code.

[next](TUTORIAL_2.md)
