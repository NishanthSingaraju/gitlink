import os

from gitlink.secret_resolvers.source import BaseSource

class EnvironmentSource(BaseSource.BaseSource):

    def resolve_secret(self, secret_name):
        secret_path = self.prepare_secret_path()
        secret_value = os.environ.get(secret_name)
        secret_file = secret_path / secret_name
        with secret_file.open("w") as f:
            f.write(secret_value)
        

        
        
