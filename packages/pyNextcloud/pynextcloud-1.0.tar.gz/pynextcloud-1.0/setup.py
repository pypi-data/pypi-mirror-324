from setuptools import setup, find_packages
from pathlib import Path


# Read the contents of README.md
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='pyNextcloud',
    version='1.0',
    description='A Python library for interacting with Nextcloud via WebDAV',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',  # Add your GitHub or documentation link here
    author='Mahir Shah',
    author_email='dev@mahirshah.dev',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    keywords='nextcloud webdav file-management',
    packages=find_packages(),
    install_requires=['requests'],
    python_requires='>=3.6',
)
