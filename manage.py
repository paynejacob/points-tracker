from flask.ext.script import Manager
from points_tracker.app import app

manager = Manager(app)

# overriding default runserver to enable debugging
@manager.command
def runserver():
    app.debug = True
    app.run()

if __name__ == "__main__":
    manager.run()
