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
        dir_path = os.path.dirname(os.path.realpath(__file__))
        meta_yaml_filepath = os.path.join(dir_path, "test_meta.yaml")
        project_metadata_filepath = os.path.join(dir_path, "test_setup.cfg")

        add_to_run_requirements = []
        add_to_test_requirements = ["graphviz !=2.47.2"]

        cmeta = create_feedstock_meta_yaml(
            project,
            pypi_version,
            project_metadata_filepath=project_metadata_filepath,
            meta_yaml_filepath=meta_yaml_filepath,
            add_to_run_requirements=add_to_run_requirements,
            add_to_test_requirements=add_to_test_requirements,
        )
        expected_run_reqs = [
            "click >=7.0.0",
            "cloudpickle >=1.5.0",
            "dask >=2021.10.0",
            "distributed >=2021.10.0",
            "holidays >=0.13",
            "numpy >=1.21.0",
            "pandas >=1.3.0",
            "psutil >=5.6.6",
            "python >=3.7.*",
            "scipy >=1.3.3",
            "tqdm >=4.32.0",
            "woodwork >=0.16.2",
        ]
        expected_run_reqs = sorted(expected_run_reqs)
        expected_test_reqs = [
            "boto3 >=1.17.46",
            "composeml >=0.8.0",
            "graphviz !=2.47.2",
            "moto >=3.0.7",
            "pip >=21.3.1",
            "pyarrow >=3.0.0",
            "pympler >=0.8",
            "pytest >=7.1.2",
            "pytest-cov >=3.0.0",
            "pytest-xdist >=2.5.0",
            "python-graphviz >=0.8.4",
            "smart_open >=5.0.0",
            "urllib3 >=1.26.5",
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
        assert cmeta.meta["build"]["number"] == 0


if __name__ == "__main__":
    unittest.main()
