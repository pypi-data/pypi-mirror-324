from setuptools import setup, find_packages

setup(
    name='icm20602',
    version='0.2.2',
    packages=find_packages(),
    install_requires=[
        'spidev'
    ],
    author='Kagan Kongare',
    author_email='kagan.kongar@gmail.com',
    description='A Python library for ICM20602 sensor, Raspberry PI ready',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/kagankongar/ICM20602',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)