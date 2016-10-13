from setuptools import setup, find_packages
from taiga_contrib_saml_auth import __version__ as version

setup(
        name='taiga-contrib-saml-auth',
        version=version,
        description="The Taiga plugin for SAML authentication",
        long_description="",
        keywords='taiga, saml, auth, plugin',
        author='Jonathan Giannuzzi',
        author_email='jonathan@giannuzzi.be',
        url='https://github.com/jgiannuzzi/taiga-contrib-saml-auth',
        license='AGPL',
        include_package_data=True,
        packages=find_packages(),
        install_requires=[
            'python3-saml',
            ],
        classifiers=[
            "Programming Language :: Python",
            'Development Status :: 4 - Beta',
            'Framework :: Django',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: GNU Affero General Public License v3',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Internet :: WWW/HTTP',
            ],
        )
