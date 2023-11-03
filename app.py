from api import create_app
from api.handlers import auth, user, project, doc_place, docs, files, message


if __name__ == '__main__':
    create_app().run(debug=True)
