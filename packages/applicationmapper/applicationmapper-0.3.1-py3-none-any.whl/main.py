#!/usr/bin/env python3
from pathlib import Path
from typing import cast

import flask
import yaml
from databind.json import load as deserialize
from kubernetes.client.api_client import ApiClient
from kubernetes.config import load_config  # type: ignore[attr-defined]
from loguru import logger
from metacontroller_api.contrib.flask import MetacontrollerBlueprint
from typer import Argument, Option, Typer

from applicationmapper import ApplicationMapperController, ApplicationMapperSpec, ExecutionContext, JsonValue

app = Typer(
    no_args_is_help=True,
    pretty_exceptions_enable=False,
    rich_markup_mode="markdown",
)


@app.command()
def execute(
    manifest: Path = Argument(..., help="Path to a YAML file that contains a single `ApplicationMapper` resource."),
    secrets: list[str] = Option(
        [],
        "--secret",
        help="Mock a secret (or single secret key) that may need to be resolved by the resource via the command line "
        'in one of the following formats: `namespace/name/key=value`, `namespace/name={"key": "value"}` or '
        "`namespace/name=@<file>`. In the `@<file>` mode, the contents of the file must be a YAML-object.",
        rich_help_panel="Parameterization",
        metavar="SECRET",
    ),
    inputs: list[str] = Option(
        [],
        "--input",
        help="Mock an input that is used instead of executing an `inputQuery`. The input can be "
        "specified as `name=<YAML>` or `name=@<file>`. In the `@<file>` mode, the contents of the file must be a "
        "YAML-object.",
        rich_help_panel="Parameterization",
        metavar="INPUT",
    ),
) -> None:
    resource = yaml.safe_load(manifest.read_text())
    spec = deserialize(resource["spec"], ApplicationMapperSpec)

    # Perse --secret options.
    provided_secrets: dict[str, dict[str, dict[str, str]]] = {}
    for secret in secrets:
        locator, value = secret.partition("=")[::2]
        key_parts = locator.split("/")

        match len(key_parts):
            case 3:
                namespace, name, key = key_parts
                data = {key: value}
            case 2:
                namespace, name = key_parts
                data = cast(dict[str, str], load_yaml_arg(value))
                assert isinstance(data, dict)
            case _:
                raise ValueError(f"invalid --secret '{secret}'")

        provided_secrets.setdefault(namespace, {}).setdefault(name, {}).update(data)

    # TODO: Check for unused secrets.

    # Parse --inputs.
    parsed_inputs: dict[str, JsonValue] = {}
    for input in inputs:
        name, value = input.partition("=")[::2]
        parsed_inputs[name] = load_yaml_arg(value)

    unused_inputs = parsed_inputs.keys() - {q.name for q in spec.inputQueries}
    if unused_inputs:
        logger.warning("The following --inputs were provided but are not used: {}", unused_inputs)

    # TODO: Only initialize the Kubernetes API when we absolutely need to?
    load_config()
    context = ExecutionContext(secrets=provided_secrets, inputs=parsed_inputs, client=ApiClient())
    values = spec.get_values(context)
    resources = spec.generate(resource["metadata"]["name"], values, context)
    print(yaml.safe_dump_all(resources))


@app.command()
def run() -> None:
    controller = ApplicationMapperController()
    app = flask.Flask(__name__)
    app.register_blueprint(MetacontrollerBlueprint(controller))
    app.run("0.0.0.0", 8000)


def load_yaml_arg(arg: str) -> JsonValue:
    """
    Loads a YAML object either from a file if *arg* begins with `@` and is followed by the file path, or directly
    from *arg* as a YAML-encoded string.
    """

    if arg.startswith("@"):
        arg = Path(arg).read_text()

    return cast(JsonValue, yaml.safe_load(arg))


if __name__ == "__main__":
    app()
