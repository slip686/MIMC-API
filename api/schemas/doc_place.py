from api import ma
from api.models.doc_place import DocPlaceModel


class DocPlaceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DocPlaceModel
        load_instance = True
        fields = ('place_id', 'doc_type', 'name', 'project_id', 'parent_place_id')


doc_place_schema = DocPlaceSchema()
doc_place_schemas = DocPlaceSchema(many=True)
