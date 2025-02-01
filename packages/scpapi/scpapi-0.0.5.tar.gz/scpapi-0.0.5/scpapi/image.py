from . import Client


class StandardImage(Client):
    def __init__(self, project_id: str = None, access_key: str = None, secret_key: str = None):
        super().__init__(project_id, access_key, secret_key)

    def list(self, query: dict = None):
        self.set_method("GET")
        self.set_path('/image/v2/standard-images')
        return self.invoke(query=query)
