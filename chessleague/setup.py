from setuptools import setup

setup(
    name="chessleague",
    packages=['chessleague'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask_sqlalchemy',
        'flask_fixtures',
        'flask_restful',
    ],
)
