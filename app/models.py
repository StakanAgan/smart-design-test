from app import mongo

from flask import url_for


class PaginatedAPIMixin:
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items()],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page, **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page, **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page, **kwargs) if resources.has_prev else None,
            }
        }
        return data


class Product:
    def __init__(self, title=None, description=None, params=None):
        self.id = None
        self.title = title
        self.description = description
        self.params = params

    def __repr__(self):
        return f'Product {self.title}'

    def to_dict(self):
        data = {
            'title': self.title,
            'description': self.description,
            'params': {key: value for key, value in self.params.items()}
        }
        if self.id:
            data.update({"id": str(self.id)})
        return data

    def from_dict(self, data):
        for field in ['title', 'description', 'params']:
            if field in data:
                setattr(self, field, data[field])
        if '_id' in data:
            setattr(self, 'id', data['_id'])
        return self

    def save_to_db(self, data, db_operations):
        self.from_dict(data)
        self.id = str(db_operations.insert_one(self.to_dict()).inserted_id)
