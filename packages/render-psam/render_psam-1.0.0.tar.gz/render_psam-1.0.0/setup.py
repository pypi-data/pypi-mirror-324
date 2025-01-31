import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="render_psam",
    author_email="render_psam@kavigupta.org",
    description="Wrapper around logomaker to easily render PSAMs in a variety of ways.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kavigupta/render-psam",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=["logomaker", "matplotlib", "numpy", "pandas"],
    # documentation
    project_urls={
        "Documentation": "https://render-psam.readthedocs.io/en/latest/#",
    },
)
