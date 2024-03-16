from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='shodanx',
    version='1.0.0',
    author='D.Sanjai Kumar',
    author_email='bughunterz0047@gmail.com',
    description='ShodanX is a tool to gather information of targets using shodan dorks⚡.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sanjai-AK47/ShodanX",
    packages=find_packages(),
    install_requires=[
        'aiofiles>=23.2.1',
        'aiohttp>=3.9.1',
        'art>=6.1',
        'beautifulsoup4>=4.11.1',
        'colorama>=0.4.6',
        'click>=8.1.7',
        'requests>=2.31.0',
        'anyio>=4.2.0',
        'fake_useragent>=1.2.1',
        'urllib3>=1.26.18'
    ],
    entry_points={
        'console_scripts': [
            'shodanx = shodanx.shodanx:cli'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
