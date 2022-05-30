# workflows

This repo contains [reusable workflows for GitHub Actions](https://docs.github.com/en/actions/using-workflows/reusing-workflows). We use this repo to standardize our workflows.

These files use the [workflow syntax for GitHub Actions](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions).

## dockerimage

The workflow can be referred to using a branch or tag (here's an example of using `main`):

```
edencehealth/workflows/.github/workflows/dockerimage.yml@main
```

### Inputs

input name       | required | type    | default                    | description
---------------- | -------- | ------- | -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------
`build_args`     | False    | string  | ``                         | Additional build arguments in `KEY=VALUE` format, preferrably one per line
`container_name` | True     | string  | &nbsp;                     | The base name of the docker container; e.g. just the `xyz` part of `edence/xyz:latest`
`context_path`   | False    | string  | `.`                        | The path (relative within the repo) of the directory that contains the Dockerfile
`dockerhub_org`  | False    | string  | `edence`                   | The Docker Hub organization name or username where the image should be uploaded; e.g. just the `edence` part of `edence/xyz:latest`
`github_org`     | False    | string  | `edencehealth`             | The GitHub organization name or username where the image should be uploaded; e.g. just the `edencehealth` part of `edencehealth/xyz:latest`
`platforms`      | False    | string  | `linux/amd64,linux/arm64`  | The comma-separated target platform(s) to use when building the image
`push`           | False    | boolean | True if not a pull request | Whether to push the image to the container registries (building without pushing may be useful as a PR check)

### Secrets

These refer to github secrets that need to be defined in the calling repo or the calling repo's organization.

secret name          | required | description
-------------------- | -------- | --------------------------------------------------------------------
`dockerhub_username` | True     | The Docker Hub username to use when uploading the image
`dockerhub_token`    | True     | The Docker Hub personal access token to use when uploading the image


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
    uses: edencehealth/workflows/.github/workflows/dockerimage.yml@main
    with:
      container_name: demo_etl
      context_path: etl
    secrets: inherit
    build-args: |
      DEV_BUILD=1
      FAIL_FAST=0
```
