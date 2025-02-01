from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="elrahapi",
    version="1.0.3",
    packages=find_packages(),
    description="Package personnalisé pour faciliter  le développement avec python avec fastapi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Harlequelrah",
    author_email="maximeatsoudegbovi@example.com",
    url="https://github.com/Harlequelrah/Library-ElrahAPI",
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=["fastapi[standard]>=0.112.0", "alembic>=1.13.3","virtualenv>=20.26.6","mysql-connector-python>=9.0.0"],
    entry_points={"console_scripts": ["elrahapi=elrahapi.__main__:main"]},
)
