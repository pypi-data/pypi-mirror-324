from setuptools import setup, find_packages

setup(
    name='linex_hash',
    version='0.1.0',
    description='A custom hash function library with salt, iterations, and XOR operations',
    author='lopeklol',
    author_email='pawel.kawalec2008@gmail.com',
    url='https://github.com/lopeklol/linex_hash',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)