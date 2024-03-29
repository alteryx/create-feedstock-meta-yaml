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
name: Create Feedstock PR
on:
  workflow_dispatch:
    inputs:
      version:
        description: 'released PyPI version to use (ex - v1.11.1)'
        required: true
jobs:
  create_feedstock_pr:
    name: Create Feedstock PR
    runs-on: ubuntu-latest
    steps:
      - name: Checkout inputted version
        uses: actions/checkout@v3
        with:
          repository: ${{ github.event.pull_request.head.repo.full_name }}
          ref: ${{ github.event.inputs.version }}
          path: "./featuretools"
      - name: Pull latest from upstream for user forked feedstock
        run: |
          gh auth status
          gh repo sync alteryx/featuretools-feedstock --branch main --source conda-forge/featuretools-feedstock --force
        env:
          GITHUB_TOKEN: ${{ secrets.AUTO_APPROVE_TOKEN }}
      - uses: actions/checkout@v3
        with:
          repository: alteryx/featuretools-feedstock
          ref: main
          path: "./featuretools-feedstock"
          fetch-depth: '0'
      - name: Run Create Feedstock meta YAML
        id: create-feedstock-meta
        uses: alteryx/create-feedstock-meta-yaml@v4
        with:
          project: "featuretools"
          pypi_version: ${{ github.event.inputs.version }}
          project_metadata_filepath: "featuretools/pyproject.toml"
          meta_yaml_filepath: "featuretools-feedstock/recipe/meta.yaml"
          add_to_test_requirements: "graphviz !=2.47.2"
      - name: View updated meta yaml
        run: cat featuretools-feedstock/recipe/meta.yaml
      - name: Push updated yaml
        run: |
          cd featuretools-feedstock
          git config --unset-all http.https://github.com/.extraheader
          git config --global user.email "machineOSS@alteryx.com"
          git config --global user.name "machineAYX Bot"
          git remote set-url origin https://${{ secrets.AUTO_APPROVE_TOKEN }}@github.com/alteryx/featuretools-feedstock
          git checkout -b ${{ github.event.inputs.version }}
          git add recipe/meta.yaml
          git commit -m "${{ github.event.inputs.version }}"
          git push origin ${{ github.event.inputs.version }}
      - name: Adding URL to job output
        run: |
          echo "Conda Feedstock Pull Request: https://github.com/alteryx/featuretools-feedstock/pull/new/${{ github.event.inputs.version }}" >> $GITHUB_STEP_SUMMARY
```

To install this workflow, add the file above to the following location in your repository.

```
.github
└── workflows
    └── feedstock_pr_create.yaml
```
