import click
import json
import os
import platform
import re
import sys
import requests
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from xml.etree import ElementTree as ET
from nomad_media_cli.helpers.capture_click_output import capture_click_output
from nomad_media_cli.helpers.utils import initialize_sdk
from nomad_media_cli.helpers.get_id_from_url import get_id_from_url
from nomad_media_cli.commands.common.asset.list_assets import list_assets
from nomad_media_cli.commands.common.asset.get_asset_details import get_asset_details

@click.command()
@click.option("--id", help="Asset ID, collection id, or saved search id to list the assets for.")
@click.option("--url", help="The Nomad URL of the Asset (file or folder) to download the archive for (bucket::object-key).")
@click.option("--object-key", help="Object-key only of the Asset (file or folder) to download the archive for. This option assumes the default bucket that was previously set with the `set-bucket` command.")
@click.option("--destination", default = ".", help="Local OS folder path specifying the location to download into. If this is not specified then it assumes the current folder")
@click.option("--threads", default=3, type=click.INT, help="The number of simultaneous downloads to perform. Default is 3.")
@click.option("--include-empty-folders", is_flag=True, help="Include empty folders in the download.")
@click.option("--download-proxy", is_flag=True, help="Download the assets using a proxy.")
@click.option("-r", "--recursive", is_flag=True, help="Download the assets in the subfolders also.")
@click.pass_context
def download_assets(ctx, id, url, object_key, destination, threads, include_empty_folders, download_proxy, recursive):
    """Download archive asset"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    if not id and not url and not object_key:
        click.echo(json.dumps({ "error": "Please provide an id, url or object-key" }))
        sys.exit(1)
        
    if url or object_key:
        id = get_id_from_url(ctx, url, object_key, nomad_sdk)

    try:
        if not os.path.exists(destination):
            click.echo(json.dumps({ "error": f"Destination path {destination} does not exist." }))
            sys.exit(1)
            
        if not os.path.isdir(destination):
            click.echo(json.dumps({ "error": f"Destination path {destination} is not a directory." }))
            sys.exit(1)
            
        try:
            test_file = os.path.join(destination, "test")
            with open(test_file, "w") as f:
                pass
            os.remove(test_file)
        except Exception as e:
            click.echo(json.dumps({ "error": f"Destination path {destination} is not writable." }))
            sys.exit(1)

        offset = 0
        filtered_assets = []
        while True:
            assets = capture_click_output(
                ctx,
                list_assets,
                id = id,
                page_size = 100, 
                page_offset = offset,
                order_by = "url",
                order_by_type = "ascending",
                recursive = recursive)

            if not assets or assets["totalItemCount"] == 0:
                break
                
            id_details = capture_click_output(
                ctx,
                get_asset_details,
                id = id
            ) 

            asset_items = assets["items"]
            for asset in asset_items:
                if not include_empty_folders:
                    if asset["assetTypeDisplay"] == "Folder":
                        try:
                            folder_details = capture_click_output(
                                ctx,
                                get_asset_details,
                                id = asset["id"])
                        except Exception as e:
                            continue

                        if folder_details["assetStats"]["totalContentLength"] == 0:
                            continue

                filtered_assets.append(asset)
                    
            offset += 1
        
        download_assets_exec(ctx, filtered_assets, id_details, destination, threads, download_proxy, recursive)

    except Exception as e:           
        click.echo(json.dumps({"error": f"Error downloading asset: {e}"}))
        sys.exit(1)
        
def download_assets_exec(ctx, assets, id_details, destination, threads, download_proxy, recursive):
    """Download assets in batches of 100"""
    is_folder_asset = id_details["properties"]["assetTypeDisplay"] == "Folder"
    
    if is_folder_asset:
        destination = os.path.join(destination, sanitize_path(id_details["properties"]["name"]))
        os.makedirs(destination, exist_ok=True)
        
    num_file_assets = len([asset for asset in assets if asset["assetTypeDisplay"] == "File"])    

    for batch_num in range(0, len(assets), 100):
        batch = assets[batch_num:batch_num + 100]
        download_batch(ctx, batch, threads, download_proxy, is_folder_asset, id_details, destination, num_file_assets, batch_num, recursive)

    for asset in assets:
        if "fullUrl" in asset:
            del asset["fullUrl"]

    click.echo(json.dumps(assets, indent=4))
    
def download_batch(ctx, batch, threads, download_proxy, is_folder_asset, id_details, destination, num_file_assets, batch_num, recursive):
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for idx, asset in enumerate(batch):
            try:
                asset_details = capture_click_output(
                    ctx,
                    get_asset_details,
                    id = asset["id"]
                )
            except Exception as e:
                asset["downloadStatus"] = "Failed"
                asset["downloadErrorMessage"] = str(e)
                continue                

            if download_proxy:
                content_type = asset["mediaTypeDisplay"]
                if content_type == "Video":
                    url = asset_details["properties"]["previewVideoFullUrl"]
                elif content_type == "Audio":
                    url = asset_details["properties"]["previewAudioFullUrl"]
                elif content_type == "Image":
                    url = asset_details["properties"]["previewImageFullUrl"]
                else:
                    asset["downloadStatus"] = "Failed"
                    asset["downloadErrorMessage"] = "Proxy download is not supported for this media type."
                    continue
            else:
                url = asset["fullUrl"]
                
            asset_name = id_details["properties"]["displayName"]
            asset_date = id_details["properties"]["displayDate"]
            
            if is_folder_asset:
                id_url = id_details["properties"]["url"]
                asset_url = asset["url"]
                path = asset_url.replace(id_url, "")
                path = sanitize_path(path)
            else:
                path = sanitize_path(asset_name)

            # is folder
            if not url:
                if not recursive:
                    continue
                os.makedirs(f"{destination}/{path}", exist_ok=True)
            else:
                if destination:
                    path = f"{destination}/{path}"              

                asset_name = os.path.basename(path)
                print(f"({idx + 1 + 100 * batch_num}/{num_file_assets}) Downloading {asset_name}", file=sys.stderr)
                if os.path.exists(path):
                    print(f"Skipping {asset_name} as it already exists", file=sys.stderr)
                    asset["downloadStatus"] = "Skipped"
                    continue

                retries = 3
                for _ in range(retries):
                    try:                
                        response = requests.get(url, timeout=10)
                        response.raise_for_status()
                        break

                    except Exception as e:
                        asset["downloadStatus"] = "Failed"
                        asset["downloadErrorMessage"] = str(e)
                        
                if asset["downloadStatus"] == "Failed":
                    continue
                        
                if response.status_code == 200:
                    with open(path, "wb") as f:
                        f.write(response.content)
    
                    asset["downloadStatus"] = "Downloaded"
    
                    try:
                        if "." in asset_date:
                            sys_time = datetime.strptime(asset_date, "%Y-%m-%dT%H:%M:%S.%fZ").timestamp()
                        else:
                            sys_time = datetime.strptime(asset_date, "%Y-%m-%dT%H:%M:%SZ").timestamp()
    
                        os.utime(path, (sys_time, sys_time))
                    except Exception as e:
                        print(f"Error setting file time for {asset_name}: {e}", file=sys.stderr)
                    
                else:
                    asset["downloadStatus"] = "Failed"
                    downloadErrorMessage = None
                    try:
                        root = ET.fromstring(response.text)
                        error_code = root.find("Code").text
                        error_message = root.find("Message").text
                        downloadErrorMessage = f"{error_code}: {error_message}"
                    except ET.ParseError:
                        downloadErrorMessage = response.text
                        
                    asset["downloadErrorMessage"] = downloadErrorMessage

    
def sanitize_path(path):
    """Sanitize the path by replacing invalid characters with underscores (_)."""

    if path.endswith("/"):
        path = path[:-1]

    if get_target_os(path) == "Windows":
        invalid_chars = r'[<>:"\\|?*]'
    
    sanitized_path_parts = []
    for part in path.split(os.sep):
        sanitized_part = re.sub(invalid_chars, "_", part)
        sanitized_path_parts.append(sanitized_part)
        
    sanitized_path = os.sep.join(sanitized_path_parts)

    return sanitized_path

def get_target_os(path):
    """Get the target OS for the path."""
    if platform.system() == "Windows" or platform.system() == "Microsoft":
        return "Windows"
    
    abs_path = os.path.abspath(path)
    
    if abs_path.startswith("/mnt/") or abs_path.startswith("/media/"):
        return "Windows"
    
    return "Unix"