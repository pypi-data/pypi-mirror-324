from . import Client


class ServerGroup(Client):
    def __init__(self, project_id: str = None, access_key: str = None, secret_key: str = None):
        super().__init__(project_id, access_key, secret_key)

    def list(self, query: dict = None):
        self.set_method("GET")
        self.set_path('/server-group/v2/server-groups')
        return self.invoke(query=query)

    def detail(self, server_group_id: str):
        self.set_method("GET")
        self.set_path('/server-group/v2/server-groups/{serverGroupId}'.format(serverGroupId=server_group_id))
        return self.invoke()

    def create(self, body: dict = None):
        self.set_method("POST")
        self.set_path('/server-group/v2/server-groups')
        return self.invoke(body=body)

    def delete(self, server_group_id: str):
        self.set_method("DELETE")
        self.set_path('/server-group/v2/server-groups/{serverGroupId}'.format(serverGroupId=server_group_id))
        return self.invoke()
