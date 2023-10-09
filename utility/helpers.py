from api import app, db, abort


@app.errorhandler(404)
def not_found(e):
    response = {'status': 404, 'error': e.description}
    return response, 404


def get_object_or_404(model: db.Model, object_id: int):
    model_instance = model.query.get(object_id)
    if model_instance is None:
        abort(404, description=f"{model.__name__.removesuffix('Model')} with id={object_id} not found")
    return model_instance
