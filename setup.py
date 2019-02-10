from setuptools import setup

setup(
    name='Budget',
    version='1.0',
    py_modules=['budget'],
    include_package_data=True,
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        budget=main:cli
    ''',
)
