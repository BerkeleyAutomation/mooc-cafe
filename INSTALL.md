# Requirements:

- python 2.7
  - comes by default on most systems
  - check installed version with `python -V`
- pip: package manager for python
  - install with `sudo easy_install pip`
- django 1.5
  - install with `sudo pip install django==1.5`
- numpy
  - install with `sudo pip install numpy`

# To get started running the app:

  - clone the git repository:
    - e.g. `git clone https://github.com/BerkeleyAutomation/mooc-cafe.git`
  - `cd mooc-cafe/src/server/opinion`
  - `cp settings_local_default.py settings_local.py`
  - `python manage.py syncdb --noinput`
  - `python manage.py createsuperuser --username=admin --email=admin@example.com --noinput`
  - load a database, see below
  - `python manage.py runserver`
  - open a web browser to `http://localhost:8000`

# To load a database dump

  - `cd mooc-cafe/src/server/opinion`
  - `python manage.py loaddata file.json`

# To interactively query database:

  - `python manage.py shell`
  - `>>> from opinion_core.models import *`
  - `>>> DiscussionComment.objects.all()`

# To run a script:

  - copy an example from `scripts/` that sounds similar
  - from the `opinion/` directory, run `python scripts/script.py`

# To create a database dump

  - `cd mooc-cafe/src/server/opinion`
  - `python manage.py dumpdata --exclude contenttypes > file.json`
