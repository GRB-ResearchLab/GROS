from setuptools import setup, find_packages

setup(
    name='gros',
    version='0.3.0',

    description="General Robot Operator System",
    author="GRB_ResearchLab",
    author_email="grb_researchlab@grobotsa.com",

    packages=find_packages(),
    include_package_data=True,

    install_requires=[
        'Click',
    ],
    
    entry_points='''
        [console_scripts]
        gros=gros.gros:cli
    ''',
)

