import logging

from fluidtopics.connector import LoginAuthentication, RemoteClient

from antidot.connector.generic.external_source_id_does_not_exists_error import ExternalSourceIdDoesNotExistsError


class ClientAuthentication:
    def __init__(self, function, client):
        self.function = function
        if isinstance(client, list):
            self.clients = client
        else:
            self.clients = [client]

    def __call__(self, *args, **kwargs):
        publications = self.function(*args, **kwargs)
        for client in self.clients:
            response = client.publish(*publications)
            if response.status_code == 404 and client._sender.source_id in response.content.decode("utf8"):
                logging.critical(str(ExternalSourceIdDoesNotExistsError(client)))
            return response


class LoginAndPasswordAuthentication(ClientAuthentication):
    def __init__(self, function, url, login, password, source_id):
        client = RemoteClient(url=url, authentication=LoginAuthentication(login, password), source_id=source_id)
        super(LoginAndPasswordAuthentication, self).__init__(function, client)
