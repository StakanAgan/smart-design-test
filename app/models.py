#

class PaginatedAPIMixin:
    @classmethod
    def to_collection_dict(cls, query, data, page, per_page, **kwargs):
        resources = query(data).skip(page * per_page).limit(per_page)
        data = {
            'items': [cls().to_response(item) for item in resources],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_items': query().count()
            }
        }
        return data

    def to_response(self, data):
        pass


class Product(PaginatedAPIMixin):
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

    def to_response(self, data):
        return self.from_dict(data).to_dict()

    def save_to_db(self, data, db_operations):
        self.from_dict(data)
        self.id = str(db_operations.insert_one(self.to_dict()).inserted_id)
