from pathlib import Path

import setuptools


def get_readme():
    here = Path(__file__).parent
    with open(str(Path(here, "README.md")), "r") as file:
        content = file.read()
    return content


TEST_REQUIRES = ["pytest-cov"]
SETUPTOOLS = "setuptools~=42.0.2"
VERSION = "0.3.4"

NAME = "antidot-html-connector"
setuptools.setup(
    name=NAME,
    description="HTML connector to FluidTopics",
    long_description=get_readme(),
    long_description_content_type="text/markdown",
    version=VERSION,
    author="Antidot",
    author_email="psassoulas@antidot.net",
    entry_points={"console_scripts": ["html2ft=antidot.connector.html.main:run"]},
    classifiers=[
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Development Status :: 3 - Alpha",
        "Topic :: Documentation",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
    ],
    packages=setuptools.find_namespace_packages(),
    package_dir={},
    install_requires=["beautifulsoup4", "fluidtopics>=0.2.0"],
    setup_requires=[SETUPTOOLS],
    tests_require=TEST_REQUIRES,
    extras_require={"test": TEST_REQUIRES, "setup": [SETUPTOOLS]},
    url="https://scm.mrs.antidot.net/antidot/html-connector",
    zip_safe=True,
)
