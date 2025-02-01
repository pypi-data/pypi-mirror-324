from setuptools import setup, find_packages

setup(
    name='Terriculum_first_package',  # The name of your package
    version='1.0.0',
    packages=find_packages(),  # This will find the package automatically
    install_requires=[],
    entry_points={
        'console_scripts': [
            'process-file=Terriculum_first_package.extractor:main',  # Command line tool entry point
        ],
    },
)