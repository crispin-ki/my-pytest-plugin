From playing with pytest stuff / Very rough pytest-bq equivalent plugin - from trying to understand https://github.com/Poogles/pytest-bq

There are a few other random things in here like markers and playing with config which is unnecessary for the rough pytest-bq equivalent I have done

The pytest-bq equivalent is really just two fixture factories (in conftest.py) that provide a (configged) fixure (well not configged in our case but they could be) and if I wanted I could make those two fixtures effectively a pytest plugin so it could be used across projects. Note there are a couple of other things that need doing if we want to make it configurable via ini / command line etc (addini and addoption) in the pytest_addoption hook (hooks are also interesting and used to do some custom stuff at various different places in a pytest run).

Resources:
- pytest-bq repo and also the ones that are similar (noted in that repo's README - pytest-postgresql for example)
- pytest with eric blog / articles is useful
