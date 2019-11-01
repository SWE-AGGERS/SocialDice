import datetime

from flask import Flask

from monolith.auth import login_manager
from monolith.database import db, User, Story
from monolith.views import blueprints


def create_app(debug=False):
    app = Flask(__name__)
    app.config['WTF_CSRF_SECRET_KEY'] = 'A SECRET KEY'
    app.config['SECRET_KEY'] = 'ANOTHER ONE'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///storytellers.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # DEBUGGING AND TESTING
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['TESTING'] = debug
    app.config['WTF_CSRF_ENABLED'] = not debug
    app.config['LOGIN_DISABLED'] = True

    for bp in blueprints:
        app.register_blueprint(bp)
        bp.app = app

    db.init_app(app)
    login_manager.init_app(app)
    db.create_all(app=app)

    # create a first admin user
    with app.app_context():
        q = db.session.query(User).filter(User.email == 'example@example.com')
        user = q.first()
        if user is None:
            example = User()
            example.firstname = 'Admin'
            example.lastname = 'Admin'
            example.email = 'example@example.com'
            example.dateofbirth = datetime.datetime(2020, 10, 5)
            example.is_admin = True
            example.set_password('admin')
            db.session.add(example)
            db.session.commit()

        q = db.session.query(Story).filter(Story.id == 1)
        story = q.first()
        if story is None:
            example = Story()
            example.text = 'Trial story of example admin user :)'
            example.likes = 42
            example.author_id = 1
            example.roll = {'dice': ['bike', 'tulip', 'happy', 'cat', 'ladder', 'rain']}
            example.date = datetime.datetime(2019, 11, 5)
            db.session.add(example)
            db.session.commit()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
