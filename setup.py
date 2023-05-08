from distutils.core import setup

setup(
    name="dichoseek",  # How you named your package folder (MyLib)
    packages=["dichoseek"],  # Chose the same as "name"
    version="0.2",  # Start with a small number and increase it with every change you make
    license="MIT",  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description="Performs binary search in binary files",  # Give a short description about your library
    author="Tristan Sterin",  # Type in your name
    author_email="tristan@prgm.dev",  # Type in your E-Mail
    url="https://github.com/tcosmo/dichoseek",  # Provide either the link to your github or to your website
    download_url="https://github.com/tcosmo/dichoseek/archive/refs/tags/v0.2.2.tar.gz",  # I explain this later on
    keywords=[
        "binary search",
    ],  # Keywords that define your package best
    classifiers=[
        "Development Status :: 3 - Alpha",  # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        "Intended Audience :: Developers",  # Define that your audience are developers
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",  # Again, pick a license
        "Programming Language :: Python :: 3.9",  # Specify which pyhton versions that you want to support
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
