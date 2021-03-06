from setuptools import setup, find_packages

setup(
    name="jinja",
    version="2.0.0",
    author="Marcus LaFerrera (@mlaferrera)",
    url="https://github.com/PUNCH-Cyber/stoq-plugins-public",
    license="Apache License 2.0",
    description="Decorate results using a template",
    packages=find_packages(),
    include_package_data=True,
    package_data={'jinja': ['jinja.stoq', 'stoq.tpl']},
)
