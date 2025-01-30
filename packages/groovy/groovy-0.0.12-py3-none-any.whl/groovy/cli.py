import os
import re
from urllib.parse import urlparse

import click
import gradio as gr
import huggingface_hub
from gradio_client import Client

import groovy as gv


@click.group()
def cli():
    pass


@cli.command()
def publish():
    """Publish a Groovy flow as a Gradio app"""
    click.echo(
        "This will create a new app.py file in the current directory and publish to Hugging Face Spaces\n"
    )
    flow_path = click.prompt(
        "Path to flow file in current directory", default="flow.py"
    )
    flow_name = click.prompt(
        "Name of the variable containing your Flow instance (e.g., 'my_flow' if you have 'my_flow = Flow()')",
        default="flow",
    )
    image_path = click.prompt(
        "Path to image or gif recording in current directory", default="recording.gif"
    )
    publish_all = click.confirm(
        f"Publish entire directory? (If N, only requirements.txt, {image_path}, {flow_path}, and several generated files will be published)",
        default=False,
    )

    # Convert relative path to module path
    module_path = flow_path.replace("/", ".").replace("\\", ".").rstrip(".py")

    # Create the app.py file
    app_content = f"""import gradio as gr
import groovy as gv
from {module_path} import {flow_name}

with gr.Blocks() as app:
    task_box = gr.Textbox(label="🕺 Task", value="{flow_name}.task" info="Run this workflow locally by installing the [Groovy Python package](https://github.com/abidlabs/groovy) and then running `groovy run https://huggingface.co/space/url>`.)
    with gr.Row():
        if {flow_name}.inputs:
            with gr.Column(scale=1):
                for component in {flow_name}.inputs:
                    component.render()
        with gr.Column(scale=2):
            gr.Image(label="Recording", value="{image_path}")
            config = gr.JSON(visible=False)

    @gr.on(
        triggers=[app.load] + [input.change for input in {flow_name}.inputs],
        inputs={flow_name}.inputs,
        outputs=[task_box],
        trigger_mode="always_last",
        show_api=False
    )
    def construct_prompt(*input_values):
        return {flow_name}.task.format(*input_values)

    app.load({flow_name}.to_json, None, config, api_name="flow_config")


if __name__ == "__main__":
    app.launch()
"""

    with open("app.py", "w") as f:
        f.write(app_content)

    repo_directory = os.getcwd()
    dir_name = os.path.basename(repo_directory)

    hf_api = huggingface_hub.HfApi()
    try:
        whoami = hf_api.whoami()
        if whoami["auth"]["accessToken"]["role"] != "write":
            click.echo("Need 'write' access token to create a Spaces repo.")
            huggingface_hub.login(add_to_git_credential=False)
    except OSError:
        click.echo("Need 'write' access token to create a Spaces repo.")
        huggingface_hub.login(add_to_git_credential=False)

    title = click.prompt("Enter Spaces app title", default=dir_name)
    title = format_title(title)

    click.echo(
        f"\n✨ Created app.py with `{flow_name}` from `{flow_path}`. Publishing..."
    )
    readme_file = os.path.join(repo_directory, "README.md")
    configuration = {
        "title": title,
        "app_file": "app.py",
        "sdk": "gradio",
        "sdk_version": gr.__version__,
        "hardware": "cpu-basic",
        "tags": ["groovy-flow"],
        "flow_file": flow_path,
    }
    huggingface_hub.metadata_save(readme_file, configuration)

    # Create space
    space_id = huggingface_hub.create_repo(
        configuration["title"],
        space_sdk="gradio",
        repo_type="space",
        exist_ok=True,
        space_hardware=configuration["hardware"],
    ).repo_id

    requirements_path = "requirements.txt"
    if not os.path.exists(requirements_path):
        with open(requirements_path, "w") as f:
            f.write(f"groovy=={gv.__version__}\n")

    if publish_all:
        hf_api.upload_folder(
            repo_id=space_id,
            repo_type="space",
            folder_path=repo_directory,
        )
    else:
        files_to_upload = [
            "app.py",
            flow_path,
            "README.md",
            "requirements.txt",
            image_path,
        ]
        for file in files_to_upload:
            hf_api.upload_file(
                repo_id=space_id,
                repo_type="space",
                path_in_repo=file,
                path_or_fileobj=os.path.join(repo_directory, file),
            )

    click.echo(f"🚀 Space published at https://huggingface.co/spaces/{space_id}")


def format_title(title: str):
    """Format title to be compatible with Hugging Face Spaces naming requirements"""
    title = title.replace(" ", "_")
    title = re.sub(r"[^a-zA-Z0-9\-._]", "", title)
    title = re.sub("-+", "-", title)
    while title.startswith("."):
        title = title[1:]
    return title


def resolve_space_url_to_id(space_url: str) -> str:
    """
    Resolves a Hugging Face space URL to its space ID.

    Parameters:
        space_url (str): The URL of the Hugging Face space
            e.g., 'https://huggingface.co/spaces/abidlabs/examples'
    Returns:
        str: The space ID in the format 'owner/space_name'
            e.g., 'abidlabs/examples'
    Raises:
        ValueError: If the URL is not a valid Hugging Face space URL
        ConnectionError: If there are issues connecting to the Hugging Face API
    """
    parsed_url = urlparse(space_url)
    if parsed_url.netloc not in ["huggingface.co", "www.huggingface.co"]:
        raise ValueError("Not a valid Hugging Face Space URL")
    path_parts = parsed_url.path.strip("/").split("/")
    if len(path_parts) < 3 or path_parts[0] != "spaces":
        raise ValueError("Not a valid Hugging Face Space URL")
    owner = path_parts[1]
    space_name = path_parts[2]
    return f"{owner}/{space_name}"


def load_flow_from_space(space_url: str):
    space_id = resolve_space_url_to_id(space_url)
    client = Client(space_id)
    config = client.predict(api_name="/flow_config")
    return gv.Flow.from_json(config)


@cli.command()
@click.argument("task")
def flow(task: str):
    """Launch a Groovy flow with the specified task as a string, or a URL to a Groovy Space"""
    if task.startswith(("https://", "http://")):
        flow = load_flow_from_space(task)
        flow.launch(run_immediately=False)  # For security, don't run immediately
    else:
        flow = gv.Flow(task)
        flow.launch(run_immediately=True)


def main():
    cli()
