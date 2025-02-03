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
    name='geopreprova1',
    version='0.1.1',    
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/MatteoGF',  # Your GitHub repository link
    author='Matteo Gobbi Frattini, Liang Zhongyou',  # Replace with your name
    author_email='matteo.gf@live.it',  # Replace with your email
    license='MIT',
    classifiers=classifiers,
    keywords='sentinel-1 glacier velocity offset tracking remote sensing',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
install_requires=[
    'geopandas>=0.10.0',   # Geopandas, qualsiasi versione >= 0.10.0
    'snappy>=2.0.0,<4.0.0', # Snappy tra 2.0.0 e 4.0.0
    'numpy>=1.21.0',       # NumPy, qualsiasi versione >= 1.21.0
    'matplotlib>=3.4.0',   # Matplotlib, qualsiasi versione >= 3.4.0
    'scipy>=1.6.0',        # Scipy, qualsiasi versione >= 1.6.0
    'rasterio>=1.2.0',     # Rasterio, qualsiasi versione >= 1.2.0
    'rioxarray>=0.5.0',    # Rioxarray, qualsiasi versione >= 0.5.0
    'xarray>=0.18.0',      # Xarray, qualsiasi versione >= 0.18.0
    'pyproj>=3.0.0',       # PyProj, qualsiasi versione >= 3.0.0
],

)