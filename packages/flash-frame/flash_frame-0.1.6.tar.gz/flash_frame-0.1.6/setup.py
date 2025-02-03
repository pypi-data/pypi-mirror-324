from setuptools import setup,find_packages

setup(
    name='flash-frame',
    version='0.1.6',
    python_requires=">=3.11",
    description='A simple data manipulation lib',
    author='S.Abilash',
    author_email='abinix01@gmail.com',
    packages=["flash","flash/src"],
    package_dir={'': 'flash'},
    install_requires=[
        "numpy>=2.0.1",
        "pyarrow>=19.0.0",
        "XlsxWriter>=3.2.2",
        "python-calamine>=0.3.1",
        "colorama>=0.4.6",
    ],
)
