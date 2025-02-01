from setuptools import setup, find_namespace_packages

setup(
    packages=find_namespace_packages(include=["multi_swarm*"], where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    package_data={
        "multi_swarm": ["py.typed"],
    },
) 