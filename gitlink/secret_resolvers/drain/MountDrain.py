from gitlink.secret_resolvers.drain import BaseDrain

class MountDrain(BaseDrain.BaseDrain):

    def resolve_secret(self, secret_name):
        secret_path = BaseDrain.BaseDrain._secrets_mount_dir_path() / secret_name
        if secret_path.exists() and secret_path.is_file():
            with secret_path.open() as secret_file:
                secret_value = secret_file.read()
                return secret_value