from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(
    name="simplify-lib",
    version="1.0",
    license="MIT license",
    author="antonio-cal",
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email="antonioicaldeiraicarvalho@gmail.com",
    keywords="simplify-lib",
    description="simplify-lib is for simplify many libraries of python",
    packages=["simplify-lib"],
    install_requires=["tkinter"],
)
