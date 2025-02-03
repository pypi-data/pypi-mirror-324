from setuptools import setup, find_packages

setup(
    name="dualkey",
    version="1.1.2",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "dualkey=dualkey.main:main"
        ],
    },
    author="Tanner McMullen",
    description="Encryption/decryption tool",
    license="MIT",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ilovespectra/dual.key",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

