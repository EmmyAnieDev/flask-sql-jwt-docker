from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

items = {
    1: {
     'name': 'Chair',
     'price': 15.99
    },
    2: {
       'name': 'table',
       'price': 35.99
    }
}