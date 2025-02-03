# The goblinfish.metrics.trackers Package

> Provides context-manager classes to name, track and report elapsed-time and other metrics for top-level process entry-points (like AWS Lambda Function handlers) and sub-processes within them.

## Quick Start

Install in your project:

```shell
# Install with pip
pip install goblinfish-metrics-trackers
```

```shell
# Install with pipenv
pipenv install goblinfish-metrics-trackers
```

Import in your code:

```python
from goblinfish.metrics.trackers import ProcessTracker
```

Create the timing-tracker instance:

```python
tracker = ProcessTracker()
```

Decorate your top-level/entry-point function:

```python
@tracker.track
def some_function():
    ...
```

Add any sub-process timers:

```python
@tracker.track
def some_function():
    ...

    with tracker.timer('some_process_name'):
        # Do stuff here
        ...
```

When this code is executed, after the context created by the `@tracker.track` decorator is complete, it will `print` something that looks like this:

```json
{"some_process_name": 0.0, "some_function": 0.0}
```

More detailed examples can be found in [the `examples` directory](https://bitbucket.org/stonefish-software-studio/goblinfish-metrics-process_timer-package/src/main/examples/) in the repository.

## Behavior in an `asyncio` context

This version will *work* with processes running under `asyncio`, for example:

```python
with tracker.timer('some_async_process'):
    async.run(some_function())
```

…**but** it may only capture the time needed for the async tasks/coroutines to be *created* rather than how long it takes for any of them to *execute*, depending on the implementation pattern used.
A more useful approach, shown in the `li-article-async-example.py` module in [the `examples` directory](https://bitbucket.org/stonefish-software-studio/goblinfish-metrics-process_timer-package/src/main/examples/) is to encapsulate the async processes in an async *function*, then wrap all of that function's processes that need to be timed in the context manager. For example:

```python
async def get_person_data():
    sleep_for = random.randrange(2_000, 3_000) / 1000
    print(
        f'get_person_data sleeping for {sleep_for} seconds'
    )
    with tracker.timer('get_person_data'):
        await asyncio.sleep(sleep_for)
    return {'person_data': ('Professor Plum', dict())}
```

…which will contribute to the logged/printed output in a more meaningful fashion:

```json
// get_person_data sleeping for 2.054
{
    "get_person_data": 2.0551600456237793,
    "main": 2.8084700107574463
}
```

## Contribution guidelines

At this point, contributions are not accepted — I need to finish configuring the repository, deciding on whether I want to set up automated builds for pull-requests, and probably several other items.

## Who do I talk to?

The current maintainer(s) will always be listed in the `[maintainers]` section of [the `pyproject.toml` file](https://bitbucket.org/stonefish-software-studio/goblinfish-metrics-process_timer-package/src/main/pyproject.toml) in the repository.
