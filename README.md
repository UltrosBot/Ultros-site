Ultros-site
===========

[![Code Health](https://landscape.io/github/UltrosBot/Ultros-site/falcon/landscape.svg?style=flat)](https://landscape.io/github/UltrosBot/Ultros-site/falcon)

This is the code for the new version of our site at 
[https://ultros.io](https://ultros.io).

Requirements (so far):
* Falcon
* Mako
* psycopg2
* ruamel.yaml
* SQLAlchemy
* Alembic

Setting up
----------

1. Fill out your `config.yml` based on `config.example.yml`
    * Ensure the database you gave above exists
2. Run `python3 tools.py run-migrations`
3. Set up your WSGI server of choice; the app is `ultros_site.__main__.app`
4. On your webserver, make sure you serve `/static` directly instead of proxying it to the WSGI app

Running migrations
------------------

Simply run `python3 tools.py run-migrations` again to make sure your database is up to date after every pull.

Developmers: Modifying the database
-----------------------------------

If you're going to change the database, do the following:

1. Before you edit or create a schema, ensure you run `python3 tools.py run-migrations` so that you're up-to-date
    * This is important as Alembic uses the current state of the database to generate migrations
2. Go ahead and make your edits
3. Run `python3 tools.py create-migrations "Summary of the migrations"`
4. Run `python3 tools.py run-migrations` to update your local database with the migration you just created

Advanced Alembic usage
----------------------

If you need to run Alembic manually, please ensure that you set your PYTHONPATH variable to `.` (or add `.` to it),
otherwise the Alembic environment will not be able to import the database metadata and will fail to load.
