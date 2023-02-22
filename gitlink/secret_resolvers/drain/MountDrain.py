from gitlink.secret_resolvers.drain import base_drain

class MountDrain(base_drain.SecretDrain):

    def resolve_secret(self, secret_name):
        secret_path = base_drain.SecretDrain._secrets_mount_dir_path() / secret_name
        if secret_path.exists() and secret_path.is_file():
            with secret_path.open() as secret_file:
                secret_value = secret_file.read()
        return secret_value