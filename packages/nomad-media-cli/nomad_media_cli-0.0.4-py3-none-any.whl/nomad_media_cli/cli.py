import click
from click import style

import os
from platformdirs import user_config_dir
import sys

from nomad_media_cli.commands.cli_commands.init import init
from nomad_media_cli.commands.cli_commands.list_config_path import list_config_path
from nomad_media_cli.commands.cli_commands.login import login
from nomad_media_cli.commands.cli_commands.logout import logout
from nomad_media_cli.commands.cli_commands.update_config import update_config

from nomad_media_cli.commands.admin.asset_upload.upload_assets import upload_assets

from nomad_media_cli.commands.common.asset.delete_asset import delete_asset
from nomad_media_cli.commands.common.asset.download_assets import download_assets
from nomad_media_cli.commands.common.asset.get_asset_details import get_asset_details
from nomad_media_cli.commands.common.asset.list_assets import list_assets
from nomad_media_cli.commands.common.asset.list_buckets import list_buckets
from nomad_media_cli.commands.common.asset.set_default_bucket import set_default_bucket

from nomad_media_cli.commands.common.content_metadata.add_asset_collection import add_asset_collection
from nomad_media_cli.commands.common.content_metadata.add_asset_properties import add_asset_properties
from nomad_media_cli.commands.common.content_metadata.add_asset_related_content import add_asset_related_content
from nomad_media_cli.commands.common.content_metadata.add_asset_tag import add_asset_tag
from nomad_media_cli.commands.common.content_metadata.list_asset_collections import list_asset_collections
from nomad_media_cli.commands.common.content_metadata.list_asset_related_contents import list_asset_related_contents
from nomad_media_cli.commands.common.content_metadata.list_asset_tags import list_asset_tags
from nomad_media_cli.commands.common.content_metadata.remove_asset_collection import remove_asset_collection
from nomad_media_cli.commands.common.content_metadata.remove_asset_related_content import remove_asset_related_content
from nomad_media_cli.commands.common.content_metadata.remove_asset_tag import remove_asset_tag

from nomad_media_cli.commands.common.search.get_content_definition_contents import get_content_definition_contents

from nomad_media_cli.helpers.check_token import check_token

# Set the configuration directory and path
CONFIG_DIR = user_config_dir("nomad_media_cli")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")

@click.group()
@click.option("--config-path", default=CONFIG_PATH, help="Path to the configuration file (optional)")
@click.pass_context
def cli(ctx, config_path):
    """Nomad Media CLI"""
    ctx.ensure_object(dict)
    ctx.obj["config_path"] = config_path

def add_command(command):
    #@click.command(name=command.name)
    #@click.pass_context
    #def wrapper(ctx, *args, **kwargs):
    #    with click.progressbar(length=100, label=f"Running {command.name}...", file=sys.stderr) as progress:
    #        result = ctx.invoke(command, *args, **kwargs)
    #        progress.update(100)
    #        progress.finish()  
    #    return result       

    return cli.add_command(command)   
    
# CLI_Commands
add_command(init)
add_command(list_config_path)
add_command(login)
add_command(logout)
add_command(update_config)

# Admin
# Asset Upload
add_command(upload_assets)

# Common
# Asset
add_command(delete_asset)
add_command(download_assets)
add_command(get_asset_details)
add_command(list_assets)
add_command(list_buckets)
add_command(set_default_bucket)

# Content Metadata
add_command(add_asset_collection)
add_command(add_asset_properties)
add_command(add_asset_related_content)
add_command(add_asset_tag)
add_command(list_asset_collections)
add_command(list_asset_tags)
add_command(list_asset_related_contents)
add_command(remove_asset_collection)
add_command(remove_asset_related_content)
add_command(remove_asset_tag)

# Search
add_command(get_content_definition_contents)

@cli.result_callback()
@click.pass_context
def process(ctx, *args, **kwargs):
    if ctx.obj.get("nomad_sdk"):
        check_token(ctx.obj["config_path"], ctx.obj["nomad_sdk"])

if __name__ == "__main__":
    cli(obj={})
