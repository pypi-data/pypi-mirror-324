from setuptools import setup, find_packages

setup(
    name='gpity',
    version='0.1.3',
    packages=find_packages(),
    install_requires=[
        'requests',
        'deep-translator',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
