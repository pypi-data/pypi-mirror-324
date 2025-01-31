from setuptools import setup, find_namespace_packages

setup(
    packages=find_namespace_packages(include=['multi_swarm*'], where='src'),
    package_dir={'': 'src'},
) 