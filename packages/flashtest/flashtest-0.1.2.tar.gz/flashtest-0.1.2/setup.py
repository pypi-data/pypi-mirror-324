from setuptools import setup, find_packages

setup(
    name='flashtest',
    version='0.1.2',
    description='A CLI-based penetration testing tool with reconnaissance and AI-driven exploits.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Shubham Parida',
    author_email='paridashub9871@gmail.com',
    url='https://github.com/shubham-parida01/flashtest',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'requests',  # Used for running external commands (such as dig)
        'whois',       # For WHOIS lookups
    ],
    entry_points={
        'console_scripts': [
            'flashtest=flashtest.cli:main',
        ],
    },
    python_requires='>=3.6',
)
