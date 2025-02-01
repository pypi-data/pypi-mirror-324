from setuptools import setup, find_packages

setup(
    name='pyfastdoop',
    version='1.0.1',
    description='A Python wrapper for fastdoop library with Spark',
    long_description=open('README.md').read(),  # Optional, if you have a README
    long_description_content_type='text/markdown',  # Adjust if using a different format
    author='Riccardo Ceccaroni',
    author_email='riccardo.ceccaroni@uniroma1.it',
    packages=find_packages(),
    install_requires=[
        'pyspark>=3.0.0,<4.0.0',  # Define the PySpark version or any other dependencies
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',  # Adjust license as needed
    ],
    python_requires='>=3.6',  # Define your supported Python versions
    url="https://github.com/riccardoc95/pyfastdoop",
)
