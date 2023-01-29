[back to intro](README.md)

# The development workbench

One of the attractive features of Polylith is the `development` directory setup. This should help speed up prototyping and the development process.

Essentially anything in the `development` folder is a lab or workbench for playing around and exploring things. The `development` elements are not included in any of the final bricks so you can do what you like.

Polylith talks about using the **REPL** for this. That works for many. I prefer using **Jupyter notebooks** as they also document things very nicely. So we will use notebooks in this tutorial.

The great thing about the `development` folder approach is that you can use whatever you like.

## Working out how we to generate fake data

One of our workers will fetch data from an external API. To simulate that we will write a component that generates some of this data. I would like to use `faker` to do this so the data looks realistic.

The best way to get started is to spin up a new Jupyter notebook in the `development` folder. And start playing around

[Jupyter notebook 01_fake_data.ipynb](development/01_fake_data.ipynb)

In this we now have a little function that we know works. We can now look to turn this into a `component` in on our workspace.

## Create a component to fetch data

We will name this the `fetch_data` component.

To create a new component we use the poetry plugin

    poetry poly create component --name fetch_data

This creates a python module under `components/mousetrap` called `fetch_data`

We can now move our prototype code from the notebook into this component and tidy it up. It is a 2 minute job and we are done. We also know that the logic in the code works so we are less likely to have to do a lot of debugging when we spin the stack up later. This really helps with development workflow speed.

To create the component we slot it into the component's directory, in this case in the `core.py` file, but you can put it wherever you like.

```python
# components/mousetrap/fetch_data/core.py

from faker import Faker
import random
import time

fake = Faker()


def fetch_data() -> list:
    """We will fetch a random number of geos"""
    data = []
    for i in range(random.randint(2, 8)):
        data.append(fake.location_on_land())

    time.sleep(1)  # Simulate taking time to hit an external API

    return data
```

## Expose the component 'interface'

All we now need to do is to register the **interfaces** that we want to explose from this component to other bricks. In the Polylith architecture in Python, this is implemented by adding it to the `__all__` attribute in the component's `__init__.py`. Very simply this just means that these elements are going to be accessable from the outside world and can be imported into other bricks.

For this component we only need to expose the `fetch_data()` function

```python
# components/mousetrap/fetch_data/__init__.py

from mousetrap.fetch_data.core import fetch_data

__all__ = ["fetch_data"]
```

## Register the component

Finally we need to tell Poetry that this component is part of our workspace. We do this by adding it to the `pyproject.toml` file. To do this we add to the `packages` list in that file.

```toml
packages = [
    {include = "mousetrap/fetch_data", from = "components"},
]
```

We are done!

We could now write some unit tests for this component, but I will defer that until later.

---

This was the first self-contained component. Now we can move onto creating the first asynchronous worker that uses it.

[next](TUTORIAL_3A.md)
