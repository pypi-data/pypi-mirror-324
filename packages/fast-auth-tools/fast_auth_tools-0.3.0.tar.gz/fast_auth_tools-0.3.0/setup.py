from setuptools import setup, find_packages

from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="fast-auth-tools",
    version="0.3.0",
    url="https://github.com/nihilok/auth_base",
    author="nihilok",
    author_email="nihilok@jarv.dev",
    description="Simple Authentication Library for FastAPI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["main", "fast_auth.__tests__"]),
    install_requires=[
        "fastapi",
        "python-multipart",
        "passlib",
        "bcrypt==4.0.1",
        "aiosqlite",
        "PyJWT",
        "pyyaml",
    ],
    entry_points={
        "console_scripts": [
            "fast-auth-user=fast_auth.user:main",
            "fast-auth-migrate=fast_auth.user:migrate",
        ],
    },
)
