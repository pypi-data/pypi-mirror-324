from unittest import mock
from unittest.mock import ANY

import pytest
from graphql_api import field
from graphql_api.context import GraphQLContext

from graphql_service_framework import Schema
from graphql_service_framework.service import GraphQLService
from tests.utils import BasicService


class TestService:
    @mock.patch("graphql_http_server.GraphQLHTTPServer.from_api")
    def test_create_graphql_service_config(self, mock_from_api):
        root = BasicService(hello_response="service_ab")
        config = {
            "graphiql_default": "./.graphql",
            "service_manager_path": "/test_service",
        }
        GraphQLService(root, config=config)

        mock_from_api.assert_any_call(
            api=ANY,
            root_value=root,
            graphiql_default_query="./.graphql",
            health_path="/health",
            allow_cors=True,
            auth_domain=None,
            auth_audience=None,
            auth_enabled=False,
        )

        config = {
            "graphiql_default": "./.graphql",
            "auth": {
                "enabled": "true",
                "domain": "https://auth.com",
                "audience": "myapp",
            },
        }

        GraphQLService(root, config=config)

        mock_from_api.assert_any_call(
            api=ANY,
            root_value=root,
            graphiql_default_query="./.graphql",
            health_path="/health",
            allow_cors=True,
            auth_domain="https://auth.com",
            auth_audience="myapp",
            auth_enabled=True,
        )

        config = {
            "graphiql_default": "./.graphql",
            "auth": {"enabled": "true", "audience": "myapp"},
        }

        with pytest.raises(KeyError):
            GraphQLService(root, config=config)

        config = {
            "graphiql_default": "./.graphql",
            "auth": {"enabled": "true", "domain": "https://auth.com"},
        }

        with pytest.raises(KeyError):
            GraphQLService(root, config=config)

    def test_service_graphql_middleware(self):

        class HelloWorldSchema(Schema, schema_version="4.5.6"):
            @field
            def hello(self) -> str:
                raise NotImplementedError()

        class HelloWorld(HelloWorldSchema):

            @field
            def hello(self) -> str:
                return "hello"

        def auth_middleware(next, context: GraphQLContext):
            value = next()
            return value + " world"

        service = HelloWorld(config={"middleware": [auth_middleware]}).create_service()

        client = service.client()
        response = client.get("/?query={hello}")

        assert response.status_code == 200
        assert response.text == '{"data":{"hello":"hello world"}}'
