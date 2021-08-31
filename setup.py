from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='sqla_softdelete',
    packages=['sqla_softdelete'],
    version='0.0.0',
    license='GPLv3+',
    long_description=long_description,
    long_description_content_type="text/markdown",
    description='SQLAlchemy soft delete',
    author='Kelsey Roberts (forked from Vitaly Efremov)',
    author_email='kelseyr@fair.com',
    url='https://github.com/kelseyCodes/sqla-softdelete',
    download_url='https://github.com/kelseyCodes/sqla-softdelete',
    keywords=['SQLAlchemy', 'Soft delete'],
    install_requires=[
        'sqlalchemy',
        'pytest',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)