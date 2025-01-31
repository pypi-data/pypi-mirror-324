from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='dftanalyzer',
    version='2.0.7',
    license='MIT License',
    author='Rafael Reis Barreto',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='rafinhareis17@gmail.com',
    keywords='dft,quantum espresso,siesta,vasp',
    description=u'Data visualization for DFT codes',
    packages=['dftanalyzer'],
    install_requires=['pandas','numpy','scipy','matplotlib'],)