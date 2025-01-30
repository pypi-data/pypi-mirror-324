import threading
import time

from urllib import request

from werkzeug.test import EnvironBuilder
from werkzeug.wrappers import Request

from graphql_http_server import GraphQLHTTPServer


class TestApp:
    def test_dispatch(self, schema):
        server = GraphQLHTTPServer(schema=schema)

        builder = EnvironBuilder(method="GET", query_string="query={hello}")

        req = Request(builder.get_environ())
        response = server.dispatch(request=req)

        assert response.status_code == 200
        assert response.data == b'{"data":{"hello":"world"}}'

    def test_app(self, schema):
        server = GraphQLHTTPServer(schema=schema)
        response = server.client().get("/?query={hello}")

        assert response.status_code == 200
        assert response.data == b'{"data":{"hello":"world"}}'

    def test_app_post(self, schema):
        server = GraphQLHTTPServer(schema=schema)
        response = server.client().post(data='{"query":"{hello}"}')

        assert response.status_code == 200
        assert response.data == b'{"data":{"hello":"world"}}'

    def test_health_endpoint(self, schema):
        server = GraphQLHTTPServer(schema=schema, health_path="/health")
        response = server.client().get("/health")

        assert response.status_code == 200
        assert response.data == b"OK"

    def test_graphiql(self, schema):
        server = GraphQLHTTPServer(schema=schema)
        response = server.client().get("/", headers={"Accept": "text/html"})

        assert response.status_code == 200
        assert b"GraphiQL" in response.data

    def test_no_graphiql(self, schema):
        server = GraphQLHTTPServer(schema=schema, serve_graphiql=False)
        response = server.client().get("/", headers={"Accept": "text/html"})

        assert response.status_code == 400

    def test_run_app_graphiql(self, schema):
        server = GraphQLHTTPServer(schema=schema)

        thread = threading.Thread(target=server.run, daemon=True, kwargs={"port": 5252})
        thread.start()

        time.sleep(1.0)

        req = request.Request("http://localhost:5252", headers={"Accept": "text/html"})
        response = request.urlopen(req).read()

        assert b"GraphiQL" in response

    def test_dispatch_cors_allow_headers(self, schema):
        server = GraphQLHTTPServer(schema=schema, allow_cors=True)

        builder = EnvironBuilder(method="OPTIONS")

        req = Request(builder.get_environ())
        response = server.dispatch(request=req)

        assert response.status_code == 200
        assert response.headers["Access-Control-Allow-Headers"] == "Content-Type"

        server.auth_enabled = True

        response = server.dispatch(request=req)

        assert response.status_code == 200
        assert (
            response.headers["Access-Control-Allow-Headers"]
            == "Content-Type, Authorization"
        )
