from setuptools import setup, find_packages
from setuptools import  find_namespace_packages
# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='admirepred',
    version='1.0.0',
    description='A tool to predict abundant miRNA in exosomes',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license_files = ('LICENSE.txt',),
    url='https://github.com/raghavagps/admirepred', 
    packages=find_namespace_packages(where="src"),
    package_dir={'':'src'},
    package_data={'admirepred.':['**/*'], 
    'admirepred.blast_db':['**/*'],
    'admirepred.model':['*'],
    'admirepred.data':['*'],
    'admirepred.output':['*'],
    },

    entry_points={ 'console_scripts' : ['admirepred = admirepred.python_scripts.admirepred:main']},
    include_package_data=True,
    python_requires='>=3.9',
    install_requires=[
        'numpy', 'pandas', 'scikit-learn==1.6.1','joblib','argparse' # Add any Python dependencies here
        ],
    extras_require={ "dev":["pytest>=7.0", "twine>=4.0.2"]

    }

)
