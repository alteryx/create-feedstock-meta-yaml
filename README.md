# GitHub Action - Create Feedstock Meta YAML

<p align="center">
    <a href="https://github.com/alteryx/create-feedstock-meta-yaml/actions/workflows/unit_tests.yml" target="_blank">
        <img src="https://github.com/alteryx/create-feedstock-meta-yaml/actions/workflows/unit_tests.yml/badge.svg" alt="Unit Tests" />
    </a>
    <a href="https://github.com/alteryx/create-feedstock-meta-yaml/actions/workflows/integration_tests.yaml" target="_blank">
        <img src="https://github.com/alteryx/create-feedstock-meta-yaml/actions/workflows/integration_tests.yaml/badge.svg" alt="Integration Tests" />
    </a>
</p>
<hr>

A GitHub Action to create a feedstock recipe/meta.yaml file (based on a PyPI version).

## Usage

```yaml
name: Integration Test
on:
  release:
    types: [published]
  workflow_dispatch:
    inputs:
      project:
        description: 'release version to kickoff action'
        required: true
      pypi_version:
        description: 'release version to kickoff action'
        required: true
jobs:
  integration_test:
    name: Integration Test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          repository: ${{ github.event.pull_request.head.repo.full_name }}
          ref: ${{ github.event.release.tag_name }}
      - name: Create Feedstock meta
        id: create-feedstock-meta
        uses: ./
        with:
          project: "featuretools"
          pypi_version: ${{ github.event.release.tag_name || github.event.inputs.pypi_version }}
          project_metadata_filepath: "setup.cfg"
          meta_yaml_filepath: "featuretools-feedstock/meta.yaml"
          add_to_run_requirements: ""
          add_to_test_requirements: "python-graphviz >=0.8.4"
      - name: Print output
        run: cat example_meta.yaml
      - name: Create Pull Request
        uses: peter-evans/create-pull-request@v4
        with:
          token: "${{ secrets.REPO_SCOPED_TOKEN }}"
          path: "${{ github.action_repository  }}"
          commit-message: Update meta yaml for feedstock
          title: "${{ github.action_repository }} "  "${{ github.event.release.tag_name }} - Instant"
          author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
          body: "This is an auto-generated PR with a new PyPI version."
          branch: min-dep-update
          branch-suffix: short-commit-hash
          base: main
```

To install this workflow, add the file above to the following location in your repository.

```
.github
└── workflows
    └── feedstock_pr_create.yaml
```
