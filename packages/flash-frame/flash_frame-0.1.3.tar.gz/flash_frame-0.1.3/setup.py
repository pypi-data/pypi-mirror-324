from setuptools import setup,find_packages

setup(
    name='flash-frame',
    version='0.1.3',
    python_version=">=3.11",
    description='A simple data manipulation lib',
    author='S.Abilash',
    author_email='abinix01@gmail.com',
    packages=["flash","flash/src/core"],
    install_requires=[
        "numpy>=2.0.1",
        "pyarrow>=19.0.0",
        "XlsxWriter>=3.2.2",
        "python-calamine>=0.3.1",
        "colorama>=0.4.6",
    ],
)
