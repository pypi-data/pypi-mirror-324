from setuptools import setup, find_packages

setup(
    name='Terriculum_first_package',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'process-file=Terriculum_first_package.extractor:main',  # This maps the command `process-file` to the `main` function in `extractor.py`
        ],
    },
)