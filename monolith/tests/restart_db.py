import datetime

from monolith.database import User, Story

def restart_db_tables(db, app):
    with app.app_context():
        db.init_app(app)
        db.drop_all(app=app)
        db.create_all(app=app)

        example = User()
        example.firstname = 'Admin'
        example.lastname = 'Admin'
        example.email = 'example@example.com'
        example.dateofbirth = datetime.datetime(2020, 10, 5)
        example.is_admin = True
        example.set_password('admin')
        db.session.add(example)
        db.session.commit()

        example = Story()
        example.text = 'Trial story of example admin user :)'
        example.likes = 42
        example.author_id = 1
        example.roll = {'dice': ['bike', 'tulip', 'happy', 'cat', 'ladder', 'rain']}
        example.date = datetime.datetime(2019, 11, 5)
        db.session.add(example)
        db.session.commit()



def delete_all_db(db, app):
    with app.app_context():
        db.init_app(app)
        db.drop_all(app=app)
        db.create_all(app=app)
