from setuptools import setup, find_packages

setup(
    name='Adrscheck',
    version='1.1.0',
    packages=find_packages(),
    install_requires=[],  # Add any dependencies here
    python_requires='>=3.6',
    author='SAMRUDDH K, RANJAN U',
    author_email='samruddh.k52@gmail.com, ranjanu2004@gmail.com',
    maintainer='SAMRUDDH K, RANJAN U',
    maintainer_email='samruddh.k52@gmail.com, ranjanu2004@gmail.com',
    description='This Library is a Python package designed to provide a comprehensive dataset of all addresses within the city of Mysore. It allows users to efficiently store, search, and validate addresses using a structured database. The package supports querying addresses by locality, street, pincode, and landmarks, and is designed to be easily extendable for additional features like geospatial queries or classification.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/TheAirprogrammer/Adrscheck.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    license='MIT',
)
