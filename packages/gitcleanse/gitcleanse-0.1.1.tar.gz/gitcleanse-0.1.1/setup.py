import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gitcleanse",
    version="0.1.1",
    author="Pouya Shahrdami",
    author_email="pooyashahrdami@gmail.com",
    description="A powerful command-line tool to manage your GitHub followers and following.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pouyashahrdami/GitCleanse",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        'rich',
        'requests',
        'python-dotenv'
    ],
    entry_points={
        'console_scripts': [
            'gitcleanse=main:main',
        ],
    },
    package_data={
        "": ["README.md"]
    }
)
