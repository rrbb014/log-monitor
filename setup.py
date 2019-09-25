from glob import glob
from distutils.core import setup

def find_packages():
    def convert(x):
        x = x.replace('/__init__.py', '')
        x = x.replace('/', '.') 
        return x

    raw_pkgs = glob('**/__init__.py', recursive=True)
    processed_pkgs = list(map(convert, raw_pkgs))
    return processed_pkgs

setup(
    name='gauss_keeker',
    version='1.0',
    description='Gauss ML Log event handler',
    author='Minseo Gong',
    author_email='gutssoul1@gmail.com',
    packages=find_packages()
)
