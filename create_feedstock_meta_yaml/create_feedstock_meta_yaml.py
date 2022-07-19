import configparser

import requests
from conda_forge_tick.recipe_parser import CondaMetaYAML
from packaging.requirements import Requirement

pypi_to_conda = {
    "dask[dataframe]": "dask",
    "moto[all]": "moto",
    "smart-open": "smart_open",
    "graphviz": "python-graphviz",
}


def create_feedstock_meta_yaml(
    project,
    pypi_version,
    setup_cfg_filepath,
    meta_yaml_filepath,
    run_reqs_to_add,
    test_reqs_to_add,
):

    requirements = []
    test_requirements = []

    current_meta_sha256 = None
    current_meta_version = None

    pypi_sha256 = None

    pypi_requires_python = None
    meta_requires_python = None

    pypi_version_no_v = pypi_version
    if pypi_version.startswith("v"):
        pypi_version_no_v = pypi_version[1:]

    meta_requires_python, pypi_sha256 = extract_pypi_info(project, pypi_version_no_v)

    config = configparser.ConfigParser()
    config.read(setup_cfg_filepath)

    requirements = clean_cfg_section(config["options"]["install_requires"])
    test_requirements = clean_cfg_section(config["options.extras_require"]["test"])

    run_reqs_to_add = clean_list_length_one(run_reqs_to_add)
    test_reqs_to_add = clean_list_length_one(test_reqs_to_add)

    requirements.extend(run_reqs_to_add)
    test_requirements.extend(run_reqs_to_add)

    # add python to run requirements
    requirements.append(meta_requires_python)
    requirements = sorted(requirements)

    requirements = sorted(requirements)
    test_requirements = sorted(test_requirements)

    with open(meta_yaml_filepath) as f:
        meta_yaml_as_string = f.read()

    cmeta = CondaMetaYAML(meta_yaml_as_string)
    cmeta.jinja2_vars["version"] = pypi_version_no_v
    cmeta.meta["source"]["sha256"] = pypi_sha256
    cmeta.meta["requirements"]["host"] = ["pip", meta_requires_python]
    if len(requirements) > 0:
        cmeta.meta["requirements"]["run"] = requirements
    if len(test_requirements) > 0:
        cmeta.meta["test"]["requires"] = test_requirements

    return cmeta


def extract_pypi_info(project, pypi_version_no_v):
    url = "https://pypi.python.org/pypi/{}/{}/json".format(project, pypi_version_no_v)
    r = requests.get(url)
    if r.status_code == requests.codes.ok:
        data = r.json()
    else:
        raise ValueError(
            "Request to pypi.python.org failed. Please check project name and PyPI version",
        )

    py_min_start_idx = data["info"]["requires_python"].find(">=")
    pypi_requires_python = data["info"]["requires_python"][py_min_start_idx + 2 :]
    meta_requires_python = "python >=" + pypi_requires_python + ".*"

    for x in data["urls"]:
        if x["python_version"] == "source":
            pypi_sha256 = x["digests"]["sha256"]
            break

    return meta_requires_python, pypi_sha256


def clean_cfg_section(section):
    cleaned = []
    section = section.split("\n")
    for idx, req in enumerate(section):
        if len(req) > 1:
            package = Requirement(req)
            pypi_name = package.name
            if len(package.extras) > 0:
                pypi_name = package.name + "[" + package.extras.pop() + "]"
            if pypi_name in pypi_to_conda:
                req = pypi_to_conda.pop(pypi_name) + " " + str(package.specifier)
            req = req.replace(">= ", ">=")
            cleaned.append(req)
    return cleaned


def clean_list_length_one(item):
    if isinstance(item, list) and len(item) == 1 and " " in item[0]:
        item = item[0].split(" ")
    if item == [""]:
        return None
    return item
