from setuptools import setup, find_packages

setup(
    name="NSDQ",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["requests", "pandas", "py_vollib_vectorized", "scipy", "matplotlib", "numpy"],
)
