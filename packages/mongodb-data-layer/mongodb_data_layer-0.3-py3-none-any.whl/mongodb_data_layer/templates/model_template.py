PYTHON_TEMPLATE = """

from mongodb_data_layer.base import BaseMongoModel

class {model_name}:
    
    collection_name = '{collection_name}' # Create a collection with this name in the database

"""