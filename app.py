from api import app
from api.handlers import auth, user, project, doc_place, docs, files, message, email_validation


if __name__ == '__main__':
    app.run()
