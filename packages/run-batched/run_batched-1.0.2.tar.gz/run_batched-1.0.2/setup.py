import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="run_batched",
    author_email="run-batched@kavigupta.org",
    description="Permanant cache.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kavigupta/run_batched",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=["torch", "numpy"],
    # documentation
    project_urls={
        "Documentation": "https://run-batched.readthedocs.io/en/latest/#",
    },
)
