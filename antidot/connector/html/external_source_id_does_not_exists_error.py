class ExternalSourceIdDoesNotExistsError(Exception):
    def __init__(self, client):
        if client.url.endswith("/"):
            url = client.url[:-1]
        url = "{}{}".format(url, "/admin/khub/sources")
        msg = "Please create an 'external' source with the ID '{}' at this URL '{}'".format(client.source_id, url)
        super(ExternalSourceIdDoesNotExistsError, self).__init__(msg)
