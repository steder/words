import distribute_setup
distribute_setup.use_setuptools()

from setuptools import setup, find_packages
setup(name="Words",
    version="1.0",
    packages=find_packages(),
    install_requires=[],

    # If any package contains *.txt or *.rst files, include them:
    # And include any *.msg files found in the 'hello' package, too:
    zip_safe=True,
    package_data={'': ['*.txt', '*.rst'],
                  },

    # metadata for upload to PyPI
    author="Mike Steder",
    author_email="steder@gmail.com",
    description="Words with Friends / Scrabble Solving",
    license="MIT",
    keywords="scrabble dictionary",
    url="https://github.com/steder/words",

    # entry_points={
    #     'console_scripts':
    #         ['words_console = words.console:main'],
    #     },
    test_suite="words.test_wordlib",
    # could also include long_description, download_url, classifiers, etc.
)
