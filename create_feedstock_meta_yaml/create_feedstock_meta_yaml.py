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
    add_to_run_requirements,
    add_to_test_requirements,
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

    run_requirements = clean_cfg_section(config["options"]["install_requires"])
    test_requirements = clean_cfg_section(config["options.extras_require"]["test"])

    add_to_run_requirements = clean_list_length_one(add_to_run_requirements)
    add_to_test_requirements = clean_list_length_one(add_to_test_requirements)

    if add_to_run_requirements and len(add_to_run_requirements) > 0:
        run_requirements.extend(add_to_run_requirements)

    if add_to_test_requirements and len(add_to_test_requirements) > 0:
        test_requirements.extend(add_to_test_requirements)

    # always add python to run requirements
    run_requirements.append(meta_requires_python)

    run_requirements.sort()
    test_requirements.sort()

    with open(meta_yaml_filepath) as fp:
        meta_yaml_as_string = fp.read()

    cmeta = CondaMetaYAML(meta_yaml_as_string)
    
    build_number = 0
    if cmeta.jinja2_vars["version"] == pypi_version_no_v:
        build_number = 1
        
    cmeta.jinja2_vars["version"] = pypi_version_no_v
    cmeta.meta["source"]["sha256"] = pypi_sha256
    cmeta.meta["build"]["number"] = build_number
    cmeta.meta["requirements"]["host"] = ["pip", meta_requires_python]
    cmeta.meta["requirements"]["run"] = run_requirements
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
    new_list = None
    if isinstance(item, list) and len(item) == 1 and " " in item[0]:
        new_list = item[0].split(",")
    if item == [""] or item == []:
        return new_list
    return new_list
