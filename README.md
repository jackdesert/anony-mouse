Anony-Mouse
===========

Getting Started
---------------

    git clone /path/to/amouse
    cd amouse

    # Create Virtualenv
    python3 -m venv env

    # Install dependencies
    env/bin/pip install --upgrade pip setuptools requests

    # Install the project in editable mode with its testing requirements.
    env/bin/pip install -e ".[testing]"




Run It
------

    export AMOUSE_SLACK_HOOK='your-super-cool-hook'
    env/bin/pserve development.ini


jshint
------

    jshint amouse/static/site.js


