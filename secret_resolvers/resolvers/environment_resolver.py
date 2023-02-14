import os

from gitlink.secret_resolvers.resolvers import base_resolver

class EnvironmentResolver(base_resolver.Resolver):
    def resolve_secret(self, secret_name):
        return os.environ.get(secret_name)