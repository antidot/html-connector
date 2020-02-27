from fluidtopics.connector import LoginAuthentication, RemoteClient

from antidot.connector.generic.external_source_id_does_not_exists_error import ExternalSourceIdDoesNotExistsError


class ClientAuthentication:
    def __init__(self, function, client):
        self.function = function
        self.client = client

    def __call__(self, *args, **kwargs):
        publications = self.function(*args, **kwargs)
        response = self.client.publish(*publications)
        if response.status_code == 404 and self.client._sender.source_id in response.content.decode("utf8"):
            raise ExternalSourceIdDoesNotExistsError(self.client)
        return response


class LoginAndPasswordAuthentication(ClientAuthentication):
    def __init__(self, function, login, password, url, source_id):
        client = RemoteClient(url=url, authentication=LoginAuthentication(login, password), source_id=source_id)
        super(LoginAndPasswordAuthentication, self).__init__(function, client)
