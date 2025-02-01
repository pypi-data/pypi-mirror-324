from . import Client


class FileStorage(Client):
    def __init__(self, project_id: str = None, access_key: str = None, secret_key: str = None):
        super().__init__(project_id, access_key, secret_key)

    def list(self, query: dict = None):
        self.set_method("GET")
        self.set_path('/file-storage/v3/storages')
        return self.invoke(query=query)

    # def detail(self, virtual_server_id: str):
    #     self.set_method("GET")
    #     self.set_path('/virtual-server/v3/virtual-servers/{virtualServerId}'.format(virtualServerId=virtual_server_id))
    #     return self.invoke()

    def create(self, body: dict = None):
        self.set_method("POST")
        self.set_path('/file-storage/v4/storages')
        return self.invoke(body=body)

    def delete(self, file_storage_id: str):
        self.set_method("DELETE")
        self.set_path('/file-storage/v3/storages/{fileStorageId}'.format(fileStorageId=file_storage_id))
        return self.invoke()

    def link(self,file_storage_id: str, body: dict = None):
        self.set_method("PUT")
        self.set_path('/file-storage/v4/storages/{fileStorageId}/objects/link'.format(fileStorageId=file_storage_id))
        return self.invoke(body=body)