# -*- coding: utf-8 -*-
from pony.orm import Database, Required, Json

db = Database()
db.bind(provider='sqlite', filename='database.sqlite', create_db=True)


class UserState(db.Entity):
    """ Состояние пользователя внутри сценария."""
    user_id = Required(str, unique=True)
    scenario_name = Required(str)
    step_name = Required(str)
    context = Required(Json)


db.generate_mapping(create_tables=True)
