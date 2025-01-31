import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bridgepy",
    version="0.0.0",
    author="Papan Yongmalwong",
    author_email="papillonbee@gmail.com",
    description="bridgepy is a package for playing contract bridge with hidden partner!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/papillonbee/bridgepy",
    packages=setuptools.find_packages(),
    test_suite='tests',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    install_requires=[
    ]
)
