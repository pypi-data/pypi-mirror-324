import pathlib

import setuptools

setuptools.setup(
    name="torch_tuner",
    version="0.1.0",
    description="Tuning the model values and gradients using PyTorch",
    long_description=pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    author="Mritunjay",
    author_email="mritunjay.1121@gmail.com",
    license="The Unlicense",
    project_urls={
        "Source":"https://github.com/Mritunjay1121/torch-tuner",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities"
    ],
    python_requires=">=3.9,<3.12",
    install_requires=["pathlib","setuptools"],
    packages=setuptools.find_packages(),
    include_package_data=True,
    entry_points={"console_scripts":["torch_tuner = torch_tuner.cli:main"]},
)