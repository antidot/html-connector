class ExternalSourceIdDoesNotExistsError(Exception):
    def __init__(self, client):
        url = client._sender.url
        if url.endswith("/"):
            url = url[:-1]
        url = "{}{}".format(url, "/admin/khub/sources/create")
        msg = "Please create an 'external' source with the ID '{}' at this URL '{}'".format(
            client._sender.source_id, url
        )
        msg += " If you would prefer the source to be created automatically, please also add a coment on this ticket:"
        msg += " https://jira.antidot.net/browse/FT-4795."
        super(ExternalSourceIdDoesNotExistsError, self).__init__(msg)
