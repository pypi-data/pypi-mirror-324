# testing

This direectory contains resources to help you set up a testing environment.

## Prerequisites

[Uv]: https://docs.astral.sh/uv/

- A Kubernetes cluster for testing (e.g. Kind)
- [Nyl](https://pypi.org/project/nyl/) 0.8.0+ (e.g. via [Uv]: `uv tool install nyl` or `uvx nyl`)

## Getting started

### Setting up a remote Kind cluster

Setting up a local Kind cluster is straight forward, but if you have a remote machine then you need to remember to give
it the right API server address:

```console
$ cat <<EOF | kind create cluster --image=kindest/node:v1.23.0 --name remote --config=-
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
networking:
  apiServerAddress: "49.13.117.103"
  apiServerPort: 6443
EOF
$ cat ~/.kube/config
```

### Install core components

The [base/](./base/) directory contains Nyl manifests for installing the following base components:

- [ArgoCD](https://argo-cd.readthedocs.io/en/stable/)
- [Metacontroller](https://github.com/metacontroller/metacontroller/)
- [metrics-server](https://github.com/kubernetes-sigs/metrics-server/)

Simply run

```console
$ nyl template base/ --apply
```

In order to access ArgoCD, use port-forwarding:

```console
$ kubectl port-forward -n argocd svc/argocd-server 8080:80
```

### Setup ArgoCD repo credentials (optional)

If you are looking to generate ArgoCD applications that reference Helm charts from prviate repositories, you need to
setup ArgoCD with the credentials to pull from them. The easiest way to do this is either via the UI or via the CLI.

```console
$ argocd login localhost:8080
$ argocd repocreds add https://github.com --username my-username --password github-pat
```

### Setting up a Cloudflare tunnel

For local development, you get the best UX by running applicationmapper locally. You can do this by exposing your
locally running application for example with a Cloudflare tunnel, Ngrok or the like. This example takes you through
using a Cloudflare tunnel.

```console
$ cloudflared tunnel login
# Pick a Cloudflare managed DNS zone, e.g. example.com.
$ cloudflared tunnel create my-tunnel
$ cloudflared tunnel route dns my-tunnel applicationmapper.example.com
$ cloudflared tunnel --url http://localhost:5000 run my-tunnel
```

Now you can reach your local applicationmapper instance through `https://applicationmapper.example.com`. You must use
this URL in the [`compositecontroller.yaml`](../manifests/compositecontroller.yaml) before applying.

> **Security notice**: Your local applicationmapper instance is now accessible over the public internet. You should use
> something like `./main.py run --shared-secret $(openssl rand -hex 32)` and add the `?shared-secret=` query parameter
> to the webhook URLs.

### Installing the applicationmapper CRD and controller

After setting up a Cloudflare tunnel, you can deploy

    kubectl apply -f ../crds/applicationmapper.yaml

Now, for local development, create a Cloudflare Tunnel and update the `compositecontroller.yaml` to point to your
tunnel.

    kubectl apply -f ../manifests/compositecontroller.yaml

Then also apply the example after making suitable modifications for your tests:

    kubectl apply -f ../manifests/example.yaml
