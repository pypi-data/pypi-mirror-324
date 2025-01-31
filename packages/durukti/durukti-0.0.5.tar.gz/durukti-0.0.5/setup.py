from setuptools import setup, find_packages

ver = '0.0.5'

classifiers=[
                   "Programming Language :: Python :: 3",
                   "License :: OSI Approved :: MIT License",
                   "Operating System :: OS Independent",
               ]

# data_files = []
setup (name = 'durukti',
       version = ver,
       long_description= 'Package for writing code via AI',
       author = 'Piklu Das',
       author_email = 'pikludas86717@gmail.com',
       python_requires='>=3.10.11',
       packages=find_packages(include=['durukti','durukti' ]),
       py_modules=['durukti']
       )