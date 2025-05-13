from setuptools import setup, find_packages

setup(
    name="sydkik_backend",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "asyncpg",
        "python-dotenv",
        "google-generativeai",
        "pytest",
        "pytest-asyncio"
    ],
) 