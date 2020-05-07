import os
from setuptools import find_packages, setup

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='rijndael',
    version='0.1',
    packages=find_packages(),
    test_suite='rijndael.tests',
    include_package_data=True,
    author='flamingo',
    author_email='bulatov6@ya.ru',
    license='MIT',
    description='Rijndael // ctr',
    url='https://mssg.me/bulatov',
    classifiers=[
        'Environment :: Console',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Programming Language :: Python'
    ],
)
