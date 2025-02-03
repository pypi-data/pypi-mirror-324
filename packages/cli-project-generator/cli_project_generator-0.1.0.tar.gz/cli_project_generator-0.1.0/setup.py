from setuptools import setup, find_packages

setup(
    name="cli_project_generator",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "pydantic",
        "pydantic-settings",
        "alembic",
        "pyjwt",
        "passlib[bcrypt]",
        "python-multipart",
        "grpcio",
        "grpcio-tools",
        "strawberry-graphql"
    ],
    entry_points={
        "console_scripts": [
            "nb=cli_project_generator.main:main",
        ],
    },
    author="Nopparat",
    author_email="your.email@example.com",
    description="A CLI tool for generating FastAPI projects with WebSocket, GraphQL, and gRPC support.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/cli_project_generator",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)