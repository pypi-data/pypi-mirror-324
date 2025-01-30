from os import path
from setuptools import setup, find_packages

HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='ul-db-utils',
    version='4.0.0-alpha',
    description='Python ul db utils',
    author='Unic-lab',
    author_email='',
    url='https://gitlab.neroelectronics.by/unic-lab/libraries/common-python-utils/db-utils.git',
    packages=find_packages(include=['ul_db_utils*']),
    platforms='any',
    package_data={
        '': ['*.sql'],
        'ul_db_utils': ['py.typed'],
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            'uldbutls=ul_db_utils.main:main',
        ],
    },
    include_package_data=True,
    install_requires=[
        "py-dateutil==2.2",
        "psycogreen==1.0.2",
        "mysql-connector-python==8.0.31",
        "flask-mongoengine==1.0.0",
        "redis==4.3.4",  # 4.1.4 bu latests is 4.3.4 = because NO correct changelogs in repo
        "types-psycopg2==2.9.21.20250121",
        "types-sqlalchemy-utils==1.1.0",
        "types-redis==4.3.13",
        "types-requests==2.28.8",
        "types-jinja2==2.11.9",
        "ul-py-tool==2.0.4",
        "alembic==1.14.1",
        "blinker==1.9.0",
        "click==8.1.8",
        "colorama==0.4.6",
        "Flask==3.1.0",
        "greenlet==3.1.1",
        "itsdangerous==2.2.0",
        "Jinja2==3.1.5",
        "Mako==1.3.8",
        "MarkupSafe==3.0.2",
        "mypy==1.14.1",
        "SQLAlchemy[mypy]==2.0.37",
        "typing_extensions==4.12.2",
        "Werkzeug==3.1.3",
        "Flask-Migrate==4.1.0",
        "mypy-extensions==1.0.0",
        "Flask-SQLAlchemy==3.1.1",
        "types-SQLAlchemy==1.4.53.38",
        "psycopg2-binary==2.9.10",
        "SQLAlchemy-Utils==0.41.2",
        "types-Flask-SQLAlchemy==2.5.9.4",
    ],
)
