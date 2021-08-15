import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="CTBN",
    version="0.0.1",
    author="Brij Malhotra",
    author_email="brij.g.malhotra@gmail.com",
    description="Conditional Tree Bayesian Network for multi-label classification",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/brijml/CTBN",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        "numpy",
        "scikit-learn"
    ]
)