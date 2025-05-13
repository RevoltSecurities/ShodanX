from setuptools import setup, find_packages

with open("README.md", "r") as streamr:
    long_description = streamr.read()

setup(
    name='shodanx',
    version='1.1.0',
    author='D.Sanjai Kumar',
    author_email='bughunterz0047@gmail.com',
    description='ShodanX is a terminal-powered recon and OSINT tool built on top of the Shodan Services.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RevoltSecurities/ShodanX",
    packages=find_packages(),
    install_requires=[
        'aiodns>=3.2.0',
        'aiofiles>=24.1.0',
        'appdirs>=1.4.4',
        'art>=6.5',
        'beautifulsoup4>=4.13.4',
        'click>=8.2.0',
        'colorama>=0.4.6',
        'fake_useragent>=2.0.3',
        'httpx>=0.28.1',
        'PyYAML>=6.0.2',
        'rich>=14.0.0',
        'setuptools>=78.1.0',
        'lxml>=5.3.2',
        'bs4>=0.0.2',
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
