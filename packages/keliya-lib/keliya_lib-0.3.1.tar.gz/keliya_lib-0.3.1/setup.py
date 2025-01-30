from setuptools import setup, find_packages

setup(
    name='keliya_lib',
    version='0.3.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'boto3'
    ],
    author='Erandra Jayasundara',
    author_email='erandraj@gmail.com',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    description='AWS Lambda helpers',
    license='MIT'
)

#python3 setup.py sdist bdist_wheel
#twine upload dist/*
