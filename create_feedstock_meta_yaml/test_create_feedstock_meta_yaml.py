import os
import tempfile
import unittest

from create_feedstock_meta_yaml import create_feedstock_meta_yaml, extract_pypi_info


class TestCreateFeedstockMetaYAML(unittest.TestCase):
    def test_extract_pypi_info(self):
        meta_requires_py, pypi_sha256 = extract_pypi_info("featuretools", "v1.11.1")
        assert meta_requires_py == "python >=3.7.*"
        assert (
            pypi_sha256
            == "9c76e2ac4adcdf838f2a62beae131a627780dfe44641af59a8d146a30a4c666e"
        )

    def test_extract_pypi_info(self):
        project = "featuretools"
        pypi_version = "1.11.1"
        setup_cfg_filepath = ""
        dir_path = os.path.dirname(os.path.realpath(__file__))
        meta_yaml_filepath = os.path.join(dir_path, "example_meta.yaml")

        run_reqs_to_add = []
        test_reqs_to_add = ["python-graphviz >=0.8.4"]

        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".cfg",
            prefix="setup",
        ) as setup_cfg_file:
            setup_cfg_file.write(generate_setup_cfg_str())
            setup_cfg_file.flush()

            setup_cfg_filepath = setup_cfg_file.name

            cmeta = create_feedstock_meta_yaml(
                project,
                pypi_version,
                setup_cfg_filepath,
                meta_yaml_filepath,
                run_reqs_to_add,
                test_reqs_to_add,
            )
            expected_run_reqs = [
                "click >=7.0.0",
                "dask >=2021.10.0",
                "python >=3.7.*",
            ]
            expected_run_reqs = sorted(expected_run_reqs)
            expected_test_reqs = [
                "boto3 >=1.17.46",
                "moto >=3.0.7",
                "pip >=21.3.1",
                "python-graphviz >=0.8.4",
            ]
            expected_test_reqs = sorted(expected_test_reqs)

            assert cmeta.jinja2_vars["version"] == pypi_version
            assert (
                cmeta.meta["source"]["sha256"]
                == "9c76e2ac4adcdf838f2a62beae131a627780dfe44641af59a8d146a30a4c666e"
            )
            assert cmeta.meta["requirements"]["host"] == ["pip", "python >=3.7.*"]
            assert cmeta.meta["requirements"]["run"] == expected_run_reqs
            assert cmeta.meta["test"]["requires"] == expected_test_reqs


def generate_setup_cfg_str():
    setup_cfg_str = f"""\
    [metadata]
    name = featuretools

    [options]
    install_requires =
        click >= 7.0.0
        dask[dataframe] >= 2021.10.0
    python_requires = >=3.6, <4

    [options.extras_require]
    test =
        boto3 >= 1.17.46
        graphviz >= 0.8.4
        moto[all] >= 3.0.7
        pip >= 21.3.1
    """
    return setup_cfg_str


if __name__ == "__main__":
    unittest.main()
