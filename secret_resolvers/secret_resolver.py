from gitlink.secret_resolvers.resolvers import environment_resolver

class ResolverType(Enum):
    ENVIRONMENT = "environment"
  

class SecretResolver:
    def __init__(self, resolver_type: str, *args, **kwargs):
        self.resolver_type = ResolverType(resolver_type)
        self.resolver = None

        if self.resolver_type == ResolverType.ENVIRONMENT:
            self.resolver = environment_resolver.EnvironmentResolver()
        else:
            raise ValueError("No resolver exists")

    def resolve_secret(self, secret_name):
        return self.resolver.resolve_secret(secret_name)
