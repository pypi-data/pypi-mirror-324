from setuptools import setup

setup(
    name="cayley_permutations",
    version="1.0",
    description="A useful module",
    #    author='',
    #    author_email='foomail@foo.example',
    packages=["cayley_permutations"],  # same as name
    install_requires=["itertools", "typing"],  # external packages as dependencies
)
