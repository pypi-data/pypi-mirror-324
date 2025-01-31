from setuptools import setup, find_packages

setup(
    name='Terriculum_first_package',  # Name of the package
    version='0.2.0',                  # Version of the package
    description='A simple file processor script',
    long_description=open('README.md').read(),  # Optional: Load the README content
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your_email@example.com',
    url='https://github.com/yourusername/Terriculum_first_package',  # Your project URL (if available)
    packages=find_packages(),  # This finds all the Python packages in the directory
    classifiers=[              # Classifiers are metadata tags to help users find your package
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Adjust if you have a different license
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Minimum Python version required
    install_requires=[         # List of dependencies (if any)
        # 'some-package>=1.0',
    ],
    entry_points={  # Optional: Make your script executable from the command line
        'console_scripts': [
            'process-file = Terriculum_first_package.extractor:main',  # Your script's entry point
        ],
    },
)