from setuptools import setup, find_packages

setup(
    name="openturfpython_sdk",  # Replace with your package name
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A brief description of your SDK",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-repo/python_sdk",  # Replace with your repo
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    # install_requires=open("requirements.txt").read().splitlines(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
