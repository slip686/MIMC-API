from api import app
from api.handlers import auth, user, project, doc_place, docs, files, message

from config import Config

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, port=Config.PORT)
