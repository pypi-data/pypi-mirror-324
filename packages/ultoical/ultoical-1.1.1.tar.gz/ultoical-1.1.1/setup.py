from importlib.metadata import entry_points

from setuptools import setup, find_packages
setup(
    name="ultoical",
    version="1.1.1",
    author="totorocodesoften",
    author_email="totorocodesoften@github.com",
    description="A web app allowing you to create an ical file from your Universite de Lorraine's timetable",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/totorocodesoften/ultoical',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.10',
    install_requires=[
        "setuptools~=75.8.0",
        "gradio~=5.13.1",
        "requests~=2.32.3"
    ],
    extras_require={
    },
    entry_points={
        'console_scripts': [
            'ultoical = ultoical.__main__:main'
        ]
    },
    include_package_data=True,
    package_data={
        "": [
            "*.txt", "*.rst"
        ],
        "ultoical": [
            "data/*.dat"
        ]
    }
)