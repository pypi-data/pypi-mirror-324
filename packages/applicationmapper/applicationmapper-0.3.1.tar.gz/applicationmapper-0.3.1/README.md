# applicationmapper

[Metacontroller]: https://github.com/metacontroller/metacontroller/

This is is a Kubernetes controller implemented using [Metacontroller] that can generates ArgoCD applications
conveniently via Helm templates from input sources that are not sourced from GitOps, but instead from Rest APIs.

It is comparable to an ArgoCD `ApplicationSet` resource, but more powerful and decoupled from GitOps. The primary use
case of this controller is to manage automatic deployments of mostly homogeneous applications based on external data
sources, such as spinning up (and down) customer environments.

## Usage

The `ApplicationMapper` resource is a Cluster-scoped resource because it allows it to generate resources in any
namespace. This is relevant for being able to generate an `Application` object in the `argocd` namespace while being
able to populate `Secret` and `ConfigMap` resources in another namespace (e.g. where the application deploys its
resources to).

The template in an `ApplicationMapper` may produce any of the following resources:

- `argoproj.io/v1alpha1/Application`
- `v1/ConfigMap`
- `v1/Secret`

### Examples

- [Guestbook](./manifests/guestbooks-example.yaml) &ndash; Creates an instance of the ArgoCD Guestbook application, one
  per item in a static list of subscription IDs.
