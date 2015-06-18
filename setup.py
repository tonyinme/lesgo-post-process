from distutils.core import setup

setup(
    name='lesgo',
    version='0.1.0',
    author='Tony Martinez',
    author_email='tony.mtos@gmail.com',
    packages=['lesgo'],
    scripts=['bin/cgns_to_vdf.py', 'bin/video_cgns_to_vdf.py'],
    url='http://pypi.python.org/pypi/lesgo/',
    license='LICENSE.txt',
    description='Post processing utilities for CGNS output.',
    long_description=open('README.txt').read(),
    install_requires=["nose",
        "numpy >= 1.8.0",
        "h5py >= 2.0.0",
    ],
)

