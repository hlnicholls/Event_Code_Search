from setuptools import setup, find_packages

setup(
    name="event_code_search",
    version="0.1.0",
    author="Hannah Nicholls",
    author_email="hannahnicholls@qmul.ac.uk",
    description="A tool for searching medical event codes in the UK Biobank.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    #url="", 
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pandas>=1.1.5",
        "numpy>=1.19.5",
        "natsort>=7.1.1",
        "pyreadr>=0.4.2",
    ],
    entry_points={
        'console_scripts': [
            'event_code_search=event_code_search.__main__:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
