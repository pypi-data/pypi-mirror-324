from setuptools import setup, find_packages

setup(
    name="fastcli_autocomplete",
    version="0.1.0",
    author="wangfu",
    author_email="wangfu0811@gmail.com",
    description="A Python package to enhance CLI autocomplete performance",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/highspeed8/fastcli_autocomplete",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "fastcli_autocomplete=fastcli_autocomplete.autocomplete:fast_autocomplete",
        ],
    },
    python_requires=">=3.6",
)

