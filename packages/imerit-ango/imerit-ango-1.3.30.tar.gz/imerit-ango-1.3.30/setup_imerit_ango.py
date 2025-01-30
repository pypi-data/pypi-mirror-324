from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="imerit-ango",
    version="1.3.30",
    author="Faruk Karakaya",
    author_email="<faruk@ango.ai>",
    description="Ango-Hub SDK",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=["imerit_ango"],
    install_requires=[
        "python-socketio~=5.8.0",
        "APScheduler~=3.9.1",
        "websocket-client",
        "flask-socketio~=5.3.4",
        "requests~=2.28",
        "tqdm",
        "validators~=0.20.0",
        "boto3==1.*",
        "fastapi~=0.105.0",
        "uvicorn~=0.24.0",
        "python-dotenv~=1.0.1",
        "mangum~=0.17.0",
        "lxml~=5.2.2",
        "requests-toolbelt~=1.0.0"
    ],
    keywords=['imerit_ango', 'ango-hub', "imerit_ango sdk", "Ango", "Ango-hub"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
    ]
)
