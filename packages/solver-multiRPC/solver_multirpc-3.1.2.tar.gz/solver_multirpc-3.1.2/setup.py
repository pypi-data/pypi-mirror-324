from setuptools import setup, find_packages

setup(
    name='solver-multiRPC',
    version='3.1.2',
    author='rorschach',
    author_email='rorschach45001@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    keywords='multiRPC solver',
    url='https://github.com/SYMM-IO/solver-multiRPC.git',
    install_requires=[
        'web3>7.0.0',
        'multicallable>=6.0.0',
        'eth-account>=0.13.0',
    ],
)
