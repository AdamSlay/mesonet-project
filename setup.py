from setuptools import setup, find_packages


setup(
    name="Mesonet Take-Home Project",
    version="0.0.1",
    author="Adam Slay",
    author_email="adamslay11@gmail.com",
    description="CLI tool to read CSV file and sort by input parameter.",
    license="MIT",
    url="https://github.com/AdamSlay/mesonet-project",
    extras_require={"testing": ["pytest"]},
    packages=find_packages("src"),
    install_requires=["pandas"],
    entry_points={
        "console_scripts": [
            "rank.py = src.rank:main",
        ]
    },
)
