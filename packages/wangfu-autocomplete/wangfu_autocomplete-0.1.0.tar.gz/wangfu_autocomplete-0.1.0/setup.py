from setuptools import setup, find_packages

setup(
    name="wangfu-autocomplete",
    version="0.1.0",
    description="A Python package to make Bash autocomplete faster for CLI tools using argparse and argcomplete.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Ben",
    author_email="wangfu0811@gmail.com",
    url="https://github.com/highspeed8/python_package_publish",
    packages=find_packages(),
    install_requires=["argcomplete"],
    entry_points={
        "console_scripts": [
            "wangfu-autocomplete=wangfu_autocomplete.autocomplete:generate_bash_completion",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.6",
)
