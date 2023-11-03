from api import app
from api.handlers import auth, user, project, doc_place, docs, files, message


if __name__ == '__main__':
    app.run(debug=True)
