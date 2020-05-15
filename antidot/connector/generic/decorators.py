import logging
from typing import List, Union

from colorama import Fore, init
from fluidtopics.connector import Client, LoginAuthentication, RemoteClient

from antidot.connector.generic.external_source_id_does_not_exists_error import ExternalSourceIdDoesNotExistsError

init()


class ClientAuthentication:
    def __init__(self, function, client: Union[Client, List[Client]]):
        self.function = function
        if isinstance(client, list):
            self.clients = client
        else:
            self.clients = [client]

    def __call__(self, *args, **kwargs):
        publications = self.function(*args, **kwargs)
        if not publications:
            print(Fore.YELLOW, "/!\\ We did not have any publications to publish !", Fore.RESET)
            return None
        for client in self.clients:
            response = client.publish(*publications)
            if response.status_code == 404 and client._sender.source_id in response.content.decode("utf8"):
                error_msg = str(ExternalSourceIdDoesNotExistsError(client))
                logging.critical(error_msg)
                print(Fore.RED, error_msg, Fore.RESET)
            elif response.status_code == 200:
                successful_msg = "Uploaded everything to {} successfully : {}.".format(client, response)
                logging.info(successful_msg)
                print(Fore.GREEN, successful_msg, Fore.RESET)
            else:
                error_msg = "Problem during handling of {} : {} ({})".format(
                    client, response, response.content.decode("utf8")
                )
                logging.critical(error_msg)
                print(Fore.RED + error_msg, Fore.RESET)
        return response


class LoginAndPasswordAuthentication(ClientAuthentication):
    def __init__(self, function, url, login, password, source_id):
        client = RemoteClient(url=url, authentication=LoginAuthentication(login, password), source_id=source_id)
        super(LoginAndPasswordAuthentication, self).__init__(function, client)
