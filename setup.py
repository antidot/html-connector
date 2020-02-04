import setuptools


def get_readme():
    with open("README.md", "r") as file:
        content = file.read()
    return content


TEST_REQUIRES = ["pytest-cov"]
SETUPTOOLS = "setuptools~=42.0.2"

setuptools.setup(
    name="copro-html-connector",
    description="HTML connector to FluidTopics",
    long_description=get_readme(),
    long_description_content_type="text/markdown",
    version="0.1.2",
    author="Antidot",
    author_email="copro@antidot.net",
    entry_points={"console_scripts": ["html2ft=copro.html_connector.main:run"]},
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
    ],
    packages=setuptools.find_namespace_packages(),
    package_dir={},
    install_requires=["beautifulsoup4", "fluidtopics>=0.2.0"],
    setup_requires=[SETUPTOOLS],
    tests_require=TEST_REQUIRES,
    extras_require={"test": TEST_REQUIRES, "setup": [SETUPTOOLS]},
    url="https://scm.mrs.antidot.net/copro/html-connector",
    zip_safe=True,
)
