from setuptools import setup, find_packages


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='IPS Vagrant',
    version='0.3.0',
    description='A management utility for the (unofficial) Invision Power Suite Vagrant development box.',
    long_description=readme(),
    author='Makoto Fujimoto',
    author_email='makoto@makoto.io',
    url='https://github.com/FujiMakoto/IPS-Vagrant',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: PHP',
        'Topic :: Software Development',
        'Topic :: Software Development :: Code Generators',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities'
    ],
    packages=find_packages(),
    package_data={'ips_vagrant': ['config/*.conf', 'generators/templates/nginx/*.tpl',
                                  'generators/templates/php5-fpm/*.tpl', 'alembic.ini', 'README.rst']},
    entry_points={
        'console_scripts': [
            'ipsv = ips_vagrant.cli:cli'
        ]
    },
    install_requires=['beautifulsoup4~=4.4.1', 'mechanize~=0.2.5', 'click~=5.1', 'requests~=2.2.1', 'jinja2~=2.8',
                      'alembic~=0.8.2', 'progressbar~=2.3', 'pyOpenSSL~=0.13', 'sqlalchemy~=1.0.8']
)
