from setuptools import setup, find_packages

setup(
    name='techfinder',                            # The name of your library
    version='0.3.2',                            # The version number
    description='A Python library to detect technologies used by websites',
    long_description=open('README_EN.md').read(),  # Read long description from README
    long_description_content_type='text/markdown',
    author='Prathamesh B Anand',
    author_email='prathameshsci963@gmai.com',
    url='https://github.com/Prathameshsci369/Detector',  # Your GitHub URL
    packages=find_packages(),                   # Automatically find all packages
    install_requires=[                          # Any dependencies your package needs
        'requests==2.28.2',
        'beautifulsoup4==4.12.2',
        # Add any other dependencies you may have
    ],
    classifiers=[                               # Metadata for your package
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',  # Use MIT or another license you prefer
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',                    # Minimum Python version
)
