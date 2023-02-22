import enum

from gitlink.secret_resolvers.source import EnvironmentSource

class ResolverType(enum.Enum):
    ENVIRONMENT = "env"
  
class SecretResolver:
    def __init__(self, resolver_type: str, *args, **kwargs):
        self.resolver_type = ResolverType(resolver_type)
        self.resolver = None

        if self.resolver_type == ResolverType.ENVIRONMENT:
            self.resolver = EnvironmentSource.EnvironmentSource()
        else:
            raise ValueError("No resolver exists")

    def resolve_secret(self, secret_name):
        return self.resolver.resolve_secret(secret_name)
    
    def get_directory(self):
        return self.resolver.get_secret_path
