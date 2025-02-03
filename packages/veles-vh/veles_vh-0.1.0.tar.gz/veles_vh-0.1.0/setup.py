from setuptools import setup, find_packages

setup(
    name='veles-vh',
    version='0.1.0',
    author='Vadym Hutei',
    author_email='hutei@live.com',
    description='Miniframework for my projects',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/VadymHutei/veles',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
    install_requires=[
        'PyMySQL==1.*'
    ],
)
