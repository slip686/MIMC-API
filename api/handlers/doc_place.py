from sqlalchemy import text
from api import app, db, multi_auth
from api.models.doc_place import DocPlaceModel
from flask import request, abort
from utility.helpers import get_object_or_404


@app.route("/add_column_to_structure/<int:name>", methods=['POST'])
@multi_auth.login_required
def add_column_to_structure(name):
    if name:
        expression = text(f'ALTER TABLE doc_place_model ADD COLUMN "{name}" varchar')
        db.session.execute(expression)
        db.session.commit()
        return 'success', 200
    else:
        abort(404)


@app.route("/get_structure_columns_names")
@multi_auth.login_required
def get_structure_columns_names():
    expression = text("SELECT column_name FROM information_schema.columns WHERE table_name = 'doc_place_model'")
    result = db.session.execute(expression).fetchall()
    return {'names': [tuple(row) for row in result]}, 200


@app.route("/delete_place/<int:place_id>", methods=['DELETE'])
@multi_auth.login_required
def delete_place(place_id):
    place = get_object_or_404(DocPlaceModel, place_id)
    db.session.delete(place)
    db.session.commit()
    return 'success', 200


@app.route("/add_place/<int:project_id>/<string:doctype>", methods=['POST'])
@multi_auth.login_required
def add_place(project_id, doctype):
    if request.json.get("columns") and request.json.get("values"):
        columns = ",".join([f'"{column.strip()}"' for column in request.json.get("columns").split(',')])
        values = ",".join([f"'{value.strip()}'" for value in request.json.get("values").split('|')])

        expression = text(f"INSERT INTO doc_place_model (project_id, doc_type, {columns}) "
                          f"VALUES ({project_id}, '{doctype}', {values})")

        db.session.execute(expression)
        db.session.commit()
        return 'success', 200
    else:
        abort(404)


@app.route("/update_place", methods=['PUT'])
@multi_auth.login_required
def update_place():
    data = request.json
    if data.get("column_num") and data.get("new_value") and data.get("place_id_list"):
        place_id_list = data.get("place_id_list")
        column = data.get("column_num")
        new_value = data.get("new_value")
        expression = text(f"""UPDATE doc_place_model SET "{column}" = '{new_value}' WHERE place_id IN ({place_id_list})""")
        db.session.execute(expression)
        db.session.commit()
        return 'success', 200
    else:
        abort(404)


@app.route("/exclude_place", methods=['PUT'])
@multi_auth.login_required
def exclude_place():
    data = request.json
    if data.get("place_id") and data.get("column_num"):
        place_id = data.get("place_id")
        column = str(data.get("column_num"))
        expression = text(f'''UPDATE doc_place_model SET "{column}" = null WHERE place_id = {place_id}''')
        db.session.execute(expression)
        db.session.commit()
        return 'success', 200
    else:
        abort(404)
