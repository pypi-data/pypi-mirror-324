from setuptools import setup, find_packages

setup(
    name='shadowamino',
    version='1.0.0',
    packages=find_packages(include=['asyncshadow', 'lib', 'shadowamino']),
    install_requires=[],  
    long_description_content_type='text/markdown',
    author='Shadow',
    author_email='tmhat2374@gmail.com',
    description='Aminoapps lib for Python',
    url='https://instagram.com/po60',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    package_data={
        'asyncshadow': ['*'],
        'lib': ['*'],
        'shadowamino': ['*'],
    },
)
