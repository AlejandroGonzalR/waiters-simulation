from setuptools import setup, find_packages

setup(
    name='waiters-simularion',
    python_requires='>3.8',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'simpy>=4.0.1,<4.1.0',
        'pyhumps>=1.6.1,<1.7.0',
        'Flask>=1.1.2,<1.2.0',
        'Flask-Cors>=3.0.10,<3.1.0'
    ]
)
