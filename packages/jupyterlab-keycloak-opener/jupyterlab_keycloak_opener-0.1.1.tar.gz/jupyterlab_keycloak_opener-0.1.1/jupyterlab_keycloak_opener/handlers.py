import json
import os
import logging

from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join
import tornado

logger = Logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

class RouteHandler(APIHandler):
    # The following decorator should be present on all verb methods (head, get, post,
    # patch, put, delete, options) to ensure only authorized user can request the
    # Jupyter server
    @tornado.web.authenticated
    def get(self):
        logger.warning(f"IDPSERVER: {os.environ['IDPSERVER']}")
        self.finish(json.dumps({
            "data": os.environ['IDPSERVER']
        }))


def setup_handlers(web_app):
    host_pattern = ".*$"

    base_url = web_app.settings["base_url"]
    route_pattern = url_path_join(base_url, "jupyterlab-keycloak-opener", "idpserver")
    handlers = [(route_pattern, RouteHandler)]
    web_app.add_handlers(host_pattern, handlers)
