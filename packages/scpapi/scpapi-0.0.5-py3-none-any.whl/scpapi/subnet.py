from . import Client


class Subnet(Client):
    def __init__(self, project_id: str = None, access_key: str = None, secret_key: str = None):
        super().__init__(project_id, access_key, secret_key)

    def list(self, query: dict = None):
        self.set_method("GET")
        self.set_path('/subnet/v2/subnets')
        return self.invoke(query=query)

    def detail(self, subnet_id: str):
        self.set_method("GET")
        self.set_path('/subnet/v2/subnets/{subnetId}'.format(subnetId=subnet_id))
        return self.invoke()

    def create(self, body: dict = None):
        self.set_method("POST")
        self.set_path('/subnet/v2/subnets')
        return self.invoke(body=body)
