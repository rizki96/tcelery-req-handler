__author__ = 'rizki'

from distutils.core import setup

setup(
    name='TornadoCeleryRequest',
    version='0.1.5',
    author='Iskandar Rizki',
    author_email='iskandar.rizki@gmail.com',
    packages=['ptask_req_handler', 'tcelery_req_handler'],
    scripts=[],
    url='git+https://github.com/rizki96/tcelery-req-handler.git',
    license='LICENSE.txt',
    description='Simple routing handler for tornado-celery implementation',
    long_description=open('README.md').read(),
    install_requires=[
        "tornado == 3.2.2",
        "celery >= 3.1.0",
        "tornado-celery",
        "pika",
    ],
)