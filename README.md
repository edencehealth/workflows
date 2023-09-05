# workflows

This repo contains [reusable workflows for GitHub Actions](https://docs.github.com/en/actions/using-workflows/reusing-workflows). We use this repo to standardize our processes across projects.

These files use the [workflow syntax for GitHub Actions](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions).

## dockerimage

The workflow can be referred to using a branch or tag (here's an example of using `main`):

```
edencehealth/workflows/.github/workflows/dockerimage.yml@main
```

### Inputs

input            | required | type        | default                                        | description
---------------- | -------- | ----------- | ---------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
`build_args`     | `False`  | `'string'`  | `''`                                           | Additional build arguments in `KEY=VALUE` format, preferrably one per line
`container_name` | `True`   | `'string'`  | `'-'`                                          | The base name of the docker container; e.g. just the "xyz" part of "edence/xyz:latest"
`context_path`   | `False`  | `'string'`  | `'.'`                                          | The path (relative within the repo) of the directory that contains the Dockerfile
`dockerhub_org`  | `False`  | `'string'`  | `'edence'`                                     | The Docker Hub organization name or username where the image should be uploaded; e.g. just the "edence" part of "edence/xyz:latest"; leave blank to skip the normal Docker Hub tag
`github_org`     | `False`  | `'string'`  | `'edencehealth'`                               | The GitHub organization name or username where the image should be uploaded; e.g. just the "edencehealth" part of "edencehealth/xyz:latest"; leave blank to skip the normal GitHub tag
`platforms`      | `False`  | `'string'`  | `'linux/amd64,linux/arm64'`                    | The comma-separated target platform(s) to use when building the image
`push`           | `False`  | `'boolean'` | `"${{ github.event_name != 'pull_request' }}"` | Whether to push the image to the container registries (building without pushing may be useful as a PR check)
`push_readme`    | `False`  | `'string'`  | `''`                                           | Path of the README file to push to Docker Hub. This runs only if the dockerhub_org and container_name inputs are non-empty. The Docker Hub repo\'s long_description will be set to the contents of the given readme file. The Docker Hub short description will be set from the GitHub repo\'s description. This only runs if the "latest" image tag would be updated. (example value: "README.md")
`registry`       | `False`  | `'string'`  | `''`                                           | Server address of an additional Docker registry to log into
`registry_paths` | `False`  | `'string'`  | `''`                                           | Additional registry paths, preferrably one per line (for example "docker.io/bitnami/redis" without ":latest")
`runs_on`        | `False`  | `'string'`  | `'["ubuntu-latest"]'`                          | Quoted JSON string specifying a list of Workflow Runner machine types/labels to run the job on (note the variable name contains an underscore not a dash) - the value is processed using `fromJson`; example self-hosted runner value "[\'self-hosted\', \'linux\']"

### Secrets

secret               | required | description
-------------------- | -------- | --------------------------------------------------------------------
`dockerhub_token`    | `True`   | The Docker Hub personal access token to use when uploading the image
`dockerhub_username` | `False`  | The Docker Hub username to use when uploading the image
`registry_password`  | `False`  | Password or token used to log into the additional registry
`registry_username`  | `False`  | Username or Key ID used to log into the registry

### Example

Here's an example of how to use the workflow:

```yaml
name: docker image

on:
  push:
    paths:
      - "app/**"
      - ".github/workflows/docker.yml"
    branches:
      - main
    tags:
      - '*.*.*'

jobs:
  dockerimage:
    uses: edencehealth/workflows/.github/workflows/dockerimage.yml@main
    with:
      container_name: demoapp
      context_path: app
    secrets: inherit
```

Some arguments are multi-line arguments, here's an example of that

```yaml
name: docker image

on:
  push:
    paths:
      - "etl/**"
      - ".github/workflows/docker.yml"
    branches:
      - main
    tags:
      - '*.*.*'

jobs:
  dockerimage:
    uses: edencehealth/workflows/.github/workflows/dockerimage.yml@v1
    with:
      container_name: demo_etl
      context_path: etl
    secrets: inherit
    build-args: |
      DEV_BUILD=1
      FAIL_FAST=0
```
