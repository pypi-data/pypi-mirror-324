import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sgbridge",
    version="0.0.0",
    author="Papan Yongmalwong",
    author_email="papillonbee@gmail.com",
    description="sgbridge is a package for playing contract bridge with hidden partner!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/papillonbee/sgbridge",
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
