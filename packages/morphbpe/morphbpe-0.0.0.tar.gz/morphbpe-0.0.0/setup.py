from setuptools import setup, find_packages

setup(
    name="morphbpe",
    version="0.0.0",
    author="Ehsaneddin Asgari",
    author_email="asgari@berkeley.edu",
    description="MorphBPE: Morphologically-Aware BPE",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/llm-lab-org/MorphBPE",
    packages=find_packages(),
    install_requires=open("requirements.txt").read().splitlines(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.13",
)
