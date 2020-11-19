def get_query_from_data(data):
    query_params = {}
    for key, value in data.items():
        if isinstance(value, str) or isinstance(value, float):
            query_params.update({str(key): str(value)})
        elif isinstance(value, dict):
            data_key = next(iter(data[key]))
            value = str(data[key][data_key])
            query_params.update({f'{str(key)}.{str(data_key)}': str(value)})
