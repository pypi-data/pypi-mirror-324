from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Science/Research',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
]

setup(
    name="glaciotrack",  # Change this to your desired package name
    version="0.1.1",
    description="A Python package to process Sentinel-1 data for glacier velocity estimation.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Virginia555',  # Your GitHub repository link
    author='Virginia Valeri',  # Replace with your name
    author_email='virginiavaleri555@gmail.com',  # Replace with your email
    license='MIT',
    classifiers=classifiers,
    keywords='sentinel-1 glacier velocity offset tracking remote sensing',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
install_requires=[
    'geopandas>=0.10.0,<1.0.0',  # Geopandas version 0.10.x, but less than 1.0
    'snappy>=2.0.0,<4.0.0',       # Snappy version 3.x.x, but less than 4.0
    'numpy>=1.21.0,<2.0.0',       # NumPy version 1.21.x, but less than 2.0
    'matplotlib>=3.4.0,<4.0.0',   # Matplotlib version 3.4.x, but less than 4.0
    'scipy>=1.6.0,<2.0.0',        # Scipy version 1.6.x, but less than 2.0
],

    include_package_data=True,
    zip_safe=False,
)
