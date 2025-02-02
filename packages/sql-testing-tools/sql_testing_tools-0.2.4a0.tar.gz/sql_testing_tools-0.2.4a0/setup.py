from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    description = fh.read()


setup(
    name='sql_testing_tools',
    version='0.2.4.a',
    packages=find_packages(),
    install_requires=[
        'sqlparse>=0.5.1',
        'requests>=2.32.3'
    ],
    long_description=description,
    long_description_content_type="text/markdown",
    package_data={
        'sql_testing_tools.databases': [
            'databases/*.db'#, 
            #'./databases/bayern.db', 
            #'./databases/film_fernsehen.db',
            #'./databases/ladepunkte.db',
            #'./databases/straftaten.db',
            ]
    },
    include_package_data=True
)
