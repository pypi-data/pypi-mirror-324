from setuptools import setup, find_packages

setup(
    name="pydift",
    version="0.1.0",
    description="A simple version-tracking tool for research code development.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/alonj/pydift",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "InquirerPy==0.3.4",
        "PyYAML==6.0.2",
        "Requests==2.32.3",
    ],
    entry_points={
        "console_scripts": [
            "pydift=pydift.pydift:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)