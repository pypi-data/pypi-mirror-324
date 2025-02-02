from setuptools import setup, find_packages
setup(
    name="unnfr",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "xmltodict"
    ],
    entry_points = {
        "console_scripts": [
            'ufr=ufr.main:_main'
        ]
    },
    author="juanvel400",
    author_email="juanvel400@proton.me",
    description="A simple RSS Reader",
    license="MIT",
    url="https://github.com/juanvel4000/ufr",
    keywords="rss feed reader",
    classifiers=[
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    long_description=open('README.md', 'r').read(),
    long_description_content_type="text/markdown"
)