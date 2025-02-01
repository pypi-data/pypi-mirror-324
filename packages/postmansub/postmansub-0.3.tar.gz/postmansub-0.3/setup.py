from setuptools import setup, find_packages

# Dynamically read the version from __init__.py
def get_version():
    version = {}
    with open("postmansub/__init__.py") as f:
        exec(f.read(), version)
    return version["__version__"]

setup(
    name="postmansub",
    version=get_version(),
    description="A small package to sent post requests.",
    long_description=open("readme.md").read(),
    long_description_content_type="text/markdown",
    author="Benevant Mathew",
    author_email="benevantmathewv@gmail.com",
    license="MIT",
    packages=find_packages(include=["postmansub"]),
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "postmansub = postmansub.main:create_gui",  # entry point
        ],
    },    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",        
    ],
    python_requires=">=3.7",
)
