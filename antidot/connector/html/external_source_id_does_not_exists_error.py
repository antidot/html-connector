class ExternalSourceIdDoesNotExistsError(Exception):
    def __init__(self, client):
        print(client.__dict__)
        if client._sender.url.endswith("/"):
            url = client._sender.url[:-1]
        url = "{}{}".format(url, "admin/khub/sources/create")
        msg = "Please create an 'external' source with the ID '{}' at this URL '{}'".format(
            client._sender.source_id, url
        )
        super(ExternalSourceIdDoesNotExistsError, self).__init__(msg)
