from setuptools import setup, find_packages

setup(
    name="onelink",
    version="0.1.7",
    description="Custom OneLink generator for Android and iOS.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Jegan Rajaiya",
    author_email="jeganrajaiya@gmail.com",
    packages=find_packages(),
    install_requires=[
        'requests',  # Ensure requests is installed for URL shortening
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
