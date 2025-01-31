import subprocess
from base64 import b64decode
from dataclasses import dataclass, field
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Iterator, List, Literal, cast

import jsonpath
import requests
import yaml
from databind.json import load as deserialize
from kubernetes.client import CoreV1Api
from kubernetes.client.api_client import ApiClient
from loguru import logger
from metacontroller_api import CompositeController, CustomizeRequest, CustomizeResponse, Resource, ResourceRule, Status

from utils import enumerate_lines, indent

# Note that the order here is important due to https://github.com/NiklasRosenstein/python-databind/issues/74.
JsonValue = int | float | bool | dict[str, Any] | list[Any] | str | None


@dataclass(kw_only=True)
class SecretRef:
    namespace: str
    name: str
    key: str


@dataclass
class ValueFrom:
    secretRef: SecretRef


@dataclass(kw_only=True)
class Header:
    name: str
    valueFrom: ValueFrom
    prefixWith: str = ""
    suffixWith: str = ""


@dataclass
class HttpConfig:
    url: str
    method: Literal["GET", "POST"] = "GET"
    headers: List[Header] = field(default_factory=list)

    def execute(self, context: "ExecutionContext") -> JsonValue:
        headers = {}

        for header_config in self.headers:
            match header_config.valueFrom:
                case ValueFrom(secretRef):
                    try:
                        header_value = context.resolve_secret(secretRef)
                    except Exception as e:
                        raise ExecutionError(f"Failed to resolve secretRef {secretRef}: {e}")

            headers[header_config.name] = header_config.prefixWith + header_value + header_config.suffixWith

        try:
            response = requests.get(self.url, headers=headers)
            response.raise_for_status()
        except Exception as e:
            raise ExecutionError(f"Failed to perform {self.method} request to url '{self.url}': {e}")

        try:
            result = response.json()
        except Exception as e:
            raise ExecutionError(f"Response from {self.method} request to url '{self.url}' is not JSON: {e}")

        return result  # type: ignore[no-any-return]


@dataclass
class Transformer:
    jsonpath: str

    def transform(self, data: JsonValue) -> JsonValue:
        try:
            return jsonpath.resolve(self.jsonpath, data)  # type: ignore[arg-type, return-value]
        except jsonpath.JSONPointerError as e:
            raise ExecutionError(f"Failed to apply transformer {self}: {e}")


@dataclass
class InputQuery:
    name: str
    http: HttpConfig | None = None
    static: JsonValue = None
    transformers: List[Transformer] = field(default_factory=list)

    def __post_init__(self) -> None:
        if sum(1 for x in [self.http, self.static] if x is not None) != 1:
            raise ValueError("Need exactly one of {http|static} fields")

    def execute(self, context: "ExecutionContext") -> JsonValue:
        if self.http is not None:
            value = self.http.execute(context)
        elif self.static is not None:
            value = self.static
        else:
            assert False
        for xform in self.transformers:
            value = xform.transform(value)
        return value


@dataclass(kw_only=True)
class ApplicationMapperSpec:
    inputQueries: List[InputQuery]
    helmTemplate: str

    def iter_secret_refs(self) -> Iterator[SecretRef]:
        for query in self.inputQueries:
            if query.http:
                for header in query.http.headers:
                    yield header.valueFrom.secretRef

    def get_values(self, context: "ExecutionContext") -> JsonValue:
        values = {}
        for query in self.inputQueries:
            try:
                values[query.name] = context.resolve_input(query)
            except Exception as e:
                raise ExecutionError(f"Failed to execute query '{query.name}': {e}")
        return values

    def generate(self, resource_name: str, values: JsonValue, context: "ExecutionContext") -> list[Resource]:
        command = [
            "helm",
            "template",
            # "--debug",
        ]

        with TemporaryDirectory() as tmp:
            values_file = Path(tmp) / "values.yaml"
            values_file.write_text(yaml.safe_dump(values))

            chart_yaml = Path(tmp) / "Chart.yaml"
            chart_yaml.write_text("apiVersion: v2\nname: template\nversion: '0.0.0'\n")
            template = Path(tmp) / "templates" / "template.yaml"
            template.parent.mkdir()
            template.write_text(self.helmTemplate)
            chart = Path(tmp)

            command.append("--values")
            command.append(str(values_file))

            command.append(resource_name)
            command.append(str(chart))

            try:
                result = subprocess.run(command, text=True, capture_output=True, check=True)
            except subprocess.CalledProcessError as e:
                # TODO: This may reveal sensitive data in logs, esp. the values.
                e.add_note(f"stdout:\n{indent(e.stdout)}")
                e.add_note(f"stderr:\n{indent(e.stderr)}")
                e.add_note(f"template:\n{indent(enumerate_lines(self.helmTemplate))}\n")
                e.add_note(f"values:\n{indent(values_file.read_text())}")
                e.add_note("note:\n  set the `HELM_DEBUG=true` to pass the --debug flag.")
                raise

        return cast(list[Resource], list(filter(None, yaml.safe_load_all(result.stdout))))


class ExecutionContext:
    """
    The [`ExecutionContext`] provides details for the evaluation of an [`ApplicationMapperSpec`], such as
    inputs for secrets that can be accessed by querries for parameterization or mock inputs.

    In a regular execution of the [`ApplicationMapperController.sync()`] hook, the context owns now Kubernetes
    client with which to perform lookups. That is because we request the required secrets from Metacontroller
    instead.

    However, a Kubernetes client may be provided when executing via the CLI. This allows us to evaluate an
    [`ApplicationMapperSpec`] via the CLI without a Metacontroller deployment.
    """

    NamespacedNamedSecrets = dict[str, dict[str, dict[str, str]]]

    def __init__(
        self,
        *,
        secrets: NamespacedNamedSecrets | None = None,
        inputs: dict[str, JsonValue] | None = None,
        client: ApiClient | None = None,
    ) -> None:
        self._secrets = secrets or {}
        self._inputs = inputs or {}
        self._client = client

    def resolve_secret(self, secret_ref: SecretRef) -> str:
        try:
            return self._secrets[secret_ref.namespace][secret_ref.name][secret_ref.key]
        except KeyError as e:
            if self._client is None:
                e.add_note(f"while trying to resolve {secret_ref}")
                raise
        secret = CoreV1Api(self._client).read_namespaced_secret(secret_ref.name, secret_ref.namespace)
        assert secret.data is not None
        return b64decode(secret.data[secret_ref.key]).decode()

    def resolve_input(self, query: InputQuery) -> JsonValue:
        if query.name in self._inputs:
            return self._inputs[query.name]
        return query.execute(self)


class ExecutionError(Exception):
    pass


class ApplicationMapperController(CompositeController):
    """
    Implements a Metacontroller `CompositeController` to manage our [`ApplicationMapperSpec`] resource.
    """

    def customize(self, request: CustomizeRequest) -> CustomizeResponse:
        """
        We use the customize hook to tell Metacontroller which additional resuorces we're interested in when
        reconciling an `ApplicationMapper` resource. The resources that match the rules we return here are
        passed along to the [`sync()`] hook, allowing us to not interact with the Kubernetes API at all.
        """

        spec = deserialize(request["parent"].__getitem__("spec"), ApplicationMapperSpec)

        secret_namespace_rules: dict[str, ResourceRule] = {}
        for secret_ref in spec.iter_secret_refs():
            rule = secret_namespace_rules.setdefault(
                secret_ref.namespace,
                {"apiVersion": "v1", "resource": "secrets", "namespace": secret_ref.namespace, "names": []},
            )
            if secret_ref.name not in rule["names"]:
                rule["names"].append(secret_ref.name)

        return {"relatedResources": list(secret_namespace_rules.values())}

    def sync(self, request: CompositeController.SyncRequest) -> CompositeController.SyncResponse:
        try:
            spec = deserialize(request["parent"].__getitem__("spec"), ApplicationMapperSpec)
            secrets: ExecutionContext.NamespacedNamedSecrets = {}
            for resource in request["related"].get("Secret.v1", {}).values():
                namespace, name = resource["metadata"]["namespace"], resource["metadata"]["name"]
                secrets.setdefault(namespace, {})[name] = resource.get("data", {})
            context = ExecutionContext(secrets=secrets)
            values = spec.get_values(context)
            children = spec.generate(request["parent"]["metadata"]["name"], values, context)
            status: Status = {"state": "Ok", "error": None}
        except Exception as e:
            status = {"state": "Error", "error": str(e)}
            children = []
            logger.exception("An unhandled exception occurred in the sync hook: {}", e)

        return {"children": children, "status": status, "resyncAfterSeconds": 0}
