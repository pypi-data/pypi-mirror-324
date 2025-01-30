import click
import json
from nomad_media_cli.helpers.utils import initialize_sdk
from nomad_media_cli.helpers.get_content_definition_id import get_content_definition_id

@click.command()
@click.option("--id", help="The id of the content definition.")
@click.option("--name", help="The display name of the content definition.")
@click.option("--offset", type=click.INT, default=0, help="The offset to start from.")
@click.pass_context
def get_content_definition_contents(ctx, id, name, offset):
    """Gets the contents of a content definition"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]
    
    if id and name:
        click.echo(json.dumps({ "error": "Please provide an id or name." }))
        return

    try:
        if name:
            id = get_content_definition_id(ctx, name)
            if not id:
                click.echo(json.dumps({ "error": f"Content definition with name {name} not found." }))
                return

        result = nomad_sdk.search(None, offset, None, [{
            "fieldName": "contentDefinitionId",
            "operator": "equals",
            "values": id
        }], None, None, None, None, None, None, None, None, None, None, None)
        
        click.echo(json.dumps(result, indent=4))
        
    except Exception as e:
        click.echo(json.dumps({ "error": f"Error getting content definition contents: {e}" }))
        return