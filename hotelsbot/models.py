# -*- coding: utf-8 -*-
from pony.orm import Database, Required

db = Database()
db.bind(provider='sqlite', filename='database.sqlite', create_db=True)


class SearchHistory(db.Entity):
    """ История поиска пользователей."""
    user_id = Required(int)
    search_date = Required(str)
    command = Required(str)
    hotels = Required(str)


db.generate_mapping(create_tables=True)
