from setuptools import setup, find_packages

setup(
    name='kolonix-rag',
    version='0.1.1',
    description='A Retrieval-Augmented Generation (RAG) framework with MongoDB and Sentence Transformers',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Rino Alfian',
    author_email='rino.alpin@gmail.com',
    url='https://github.com/kolonixid/kolonix-rag',
    packages=find_packages(),
    install_requires=[
        'pymongo',
        'sentence-transformers',
        'nltk',
        'numpy'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
