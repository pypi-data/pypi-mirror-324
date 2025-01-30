import click
import sys, json

def get_content_definition_id(ctx, content_definition_name):
    """Get the content definition ID from the content definition name"""
    nomad_sdk = ctx.obj["nomad_sdk"]
    content_definitions = nomad_sdk.get_content_definitions(None, None, None, None, None)
    
    content_definition = next(filter(lambda x: x["properties"]["title"] == content_definition_name, content_definitions["items"]), None)
    
    if not content_definition:
        click.echo(json.dumps({ "error": "Content definition not found." }))
        sys.exit(1)
        
    return content_definition["contentDefinitionId"]
