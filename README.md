# GitHub Action - Create Feedstock Meta YAML

<p align="center">
    <a href="https://github.com/alteryx/create-feedstock-meta-yaml/actions/workflows/unit_tests.yml" target="_blank">
        <img src="https://github.com/alteryx/mcreate-feedstock-meta-yaml/actions/workflows/unit_tests.yml/badge.svg" alt="Unit Tests" />
    </a>
    <a href="https://github.com/alteryx/create-feedstock-meta-yaml/actions/workflows/integration_tests.yml" target="_blank">
        <img src="https://github.com/alteryx/create-feedstock-meta-yaml/actions/workflows/integration_tests.yml/badge.svg" alt="Integration Test" />
    </a>
</p>
<hr>

A GitHub Action to generate minimum Python dependencies.

## Usage

This GitHub Action provides a task to generate the minimum Python given 1 or more requirements.
```yaml
name: Create Feedstock PR
on:
  pull_request:
    types: [opened, synchronize]
jobs:
  pull_latest_main:
    name: Pull latest in forked feestock, and create feedstock PR
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          repository: ${{ github.event.pull_request.head.repo.full_name }}
          ref: ${{ github.event.release.tag_name }}
      - name: Pull latest from upstream for user forked feedstock
        run: |
          gh auth status
          rm -rf featuretools-feedstock
          gh repo fork conda-forge/featuretools-feedstock --clone
          gh repo sync machineAYX/featuretools-feedstock --branch main --source conda-forge/featuretools-feedstock --branch main --force
        env:
          GITHUB_TOKEN: ${{ secrets.AUTO_APPROVE_TOKEN }}
      - uses: actions/checkout@v3
        with:
          repository: machineAYX/featuretools-feedstock
          ref: main
      - name: Run Minimum Dependency Generator
        id: create-feedstock-meta
        uses: alteryx/create-feedstock-meta-yaml@main
        with:
          project: featuretools
          pypi_version: ${{ github.event.release.tag_name }}
          setup_cfg_filepath: setup.cfg
          meta_yaml_filepath: featuretools-feedstock/recipe/meta.yaml
          test_reqs_to_add: ["python-graphviz"]
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
