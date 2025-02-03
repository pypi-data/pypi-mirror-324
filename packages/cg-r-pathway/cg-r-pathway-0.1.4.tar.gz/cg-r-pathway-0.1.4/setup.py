from setuptools import setup, find_packages

# Read the README file with UTF-8 encoding
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='cg-r-pathway',
    version='0.1.4',  # Incremented version to avoid conflicts
    author='Bernard Kwadwo Essuman',
    author_email='simura.pathway@gmail.com',
    description='A comprehensive protein reaction coordinate optimization framework',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/simura-works/cg_r_pathway',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'numpy',
        'matplotlib',
        'torch',
        'numba',
    ],
    entry_points={
        'console_scripts': [
            'cg-r-pathway = cg_r_pathway.cli:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
    ],
    license='SIMURA License',
    python_requires='>=3.6',
)
