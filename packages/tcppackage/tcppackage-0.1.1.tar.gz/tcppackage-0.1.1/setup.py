from setuptools import setup

setup(
    name='tcppackage',
    version='0.1.1',
    packages=['tcppackage'],
    entry_points={
        'console_scripts': [
            'tcphelp = tcppackage.tcphelp:main',
            'tcprecv = tcppackage.tcprecv:main',
            'tcpsend = tcppackage.tcpsend:main',
            'tcpserv = tcppackage.tcpserv:main',
            'tcptraffic = tcppackage.tcptraffic:main',
        ],
    },
    author='Rasmnout',
    author_email='rasmnout@gmail.com (https://rasmnout.github.io)',
    description='TCP tools for network communication',
    long_description='Tools for network communication and testing using TCP.',
    long_description_content_type='text/plain',
    url='https://rasmnout.github.io',
    license='MIT',
    install_requires=[
        'scapy',
        'datetime',
        'argparse',
    ],
)

