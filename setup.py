import os

from glob import glob
from distutils.core import setup
from site import getusersitepackages

resource_dir = getusersitepackages()

def find_packages():
    def convert(x):
        x = x.replace('/__init__.py', '')
        x = x.replace('/', '.') 
        return x

    raw_pkgs = glob('**/__init__.py', recursive=True)
    processed_pkgs = list(map(convert, raw_pkgs))
    return processed_pkgs

def find_data_files(ext):
    target = "**/*.%s" % ext
    file_list = glob(target, recursive=True)
    dir_list = list(map(lambda x: os.path.split(x)[0], file_list))

    dir_file_dict = {}
    for d, f in zip(dir_list, file_list):
        if d in dir_file_dict.keys():
            dir_file_dict[d].append(f)
        else:
            dir_file_dict[d] = [f]

    result = [
            (os.path.join(resource_dir, dir_), files)
            for dir_, files 
            in dir_file_dict.items()
        ]

    return result


# If it needs to add more files, add lines below
files = find_data_files('yml')
# here



setup(
    name='ml_keeker',
    version='1.0',
    description='Gauss ML Log event monitor',
    author='Minseo Gong',
    author_email='gutssoul1@gmail.com',
    packages=find_packages(),
    data_files=files
)
