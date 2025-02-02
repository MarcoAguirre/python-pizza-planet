from dotenv import load_dotenv
from os.path import dirname, join

import pytest
from flask.cli import FlaskGroup
from flask_migrate import Migrate

from app import flask_app
from app.plugins import db
from flask_seeder import FlaskSeeder
# flake8: noqa
from app.repositories.models import Ingredient, Order, IngredientDetail, Size, Beverage

seeder = FlaskSeeder()
seeder.init_app(flask_app, db)

manager = FlaskGroup(flask_app)

migrate = Migrate()
migrate.init_app(flask_app, db)


@manager.command('test', with_appcontext=False)
def test():
    return pytest.main(['-v', './app/test'])


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

if __name__ == '__main__':
    manager()
