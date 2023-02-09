import os
from pathlib import Path
from functools import wraps
import click

import gitstore

def error_handling(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            f(*args, **kwargs)
        except ValueError as e:
            click.echo(e)
            print_help()
        except Exception as e:
            click.echo(e)
    return wrapper

def print_help():
    ctx = click.get_current_context()
    click.echo(ctx.get_help())


@click.group(name="git-store", invoke_without_command=True)
@click.pass_context
def cli_group(ctx):
    if not ctx.invoked_subcommand:
        click.echo(ctx.get_help())

@cli_group.command()
@click.argument("config")
@click.argument("build_dir", required=False)
@error_handling
def build_context(config, build_dir) -> None:
    cfg = _get_store_from_directory(config=config)
    cfg.docker_build_setup(build_dir)


@cli_group.command()
@click.argument("config", required=False)
@click.argument("build_dir", required=False)
@click.option("--tag", help="Docker image tag")
@error_handling
def build_image(config, build_dir, tag):
    cfg = _get_store_from_directory(config=config)
    if build_dir:
        build_dir = Path(build_dir)
    cfg.build_docker_image(build_dir=build_dir, tag=tag)


@cli_group.command()
@click.argument("config", required=False)
@click.argument("build_dir", required=False)
@click.option("--tag", help="Docker build image tag")
@click.option("--port", type=int, default=8080, help="Local port used to run image")
@click.option(
    "--attach", is_flag=True, default=False, help="Flag for attaching the process"
)
def run_image(config, build_dir, tag, port, attach):
    cfg = _get_store_from_directory(config=config)
    if build_dir:
        build_dir = Path(build_dir)
    cfg.run_image(build_dir=build_dir, tag=tag, local_port=port, detach=not attach)


def _get_store_from_directory(config):
    return gitstore.load(config)