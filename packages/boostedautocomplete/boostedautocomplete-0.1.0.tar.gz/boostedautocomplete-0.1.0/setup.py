from setuptools import setup, find_packages

setup(
    name="boostedautocomplete",
    version="0.1.0",
    description="Reef autocomplete",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Richard",
    author_email="richard.mccormick@reef.pl",
    url="https://github.com/richard-mccormick-reef",
    packages=find_packages(),
    install_requires=["argcomplete"],
    entry_points={
        "console_scripts":[
            "reefautocomplete=source.main:main"
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    py_modules=['reefautocomplete'],
    python_requires=">=3.6",
)