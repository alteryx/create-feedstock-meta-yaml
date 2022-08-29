from argparse import ArgumentParser

from create_feedstock_meta_yaml import create_feedstock_meta_yaml


def main():
    parser = ArgumentParser(
        description="For a given project and PyPI version, create a meta.yaml for the feedstock repo",
    )

    parser.add_argument("--project", required=True, help="name of project")

    parser.add_argument(
        "--pypi_version",
        required=True,
        help="the version of PyPI to use for the meta.yaml",
    )

    parser.add_argument(
        "--project_metadata_filepath",
        required=True,
        help="filepath of the setup.cfg or pyproject.toml (which contain core and test requirements)",
    )

    parser.add_argument(
        "--meta_yaml_filepath",
        required=True,
        help="filepath of the existing recipe/meta.yaml (in the project's feedstock repo)",
    )

    parser.add_argument(
        "--add_to_run_requirements",
        required=False,
        default=None,
        help="run requiremnts to add to the meta.yaml",
        nargs="+",
    )

    parser.add_argument(
        "--add_to_test_requirements",
        required=False,
        default=None,
        help="test requirements to add to the meta.yaml",
        nargs="+",
    )

    args = parser.parse_args()
    meta_yaml_as_str = create_feedstock_meta_yaml(
        args.project,
        args.pypi_version,
        args.project_metadata_filepath,
        args.meta_yaml_filepath,
        args.add_to_run_requirements,
        args.add_to_test_requirements,
    )
    with open(args.meta_yaml_filepath, "w") as fp:
        meta_yaml_as_str.dump(fp)


if __name__ == "__main__":
    main()
