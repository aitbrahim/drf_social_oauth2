from setuptools import setup, find_packages

version = '0.2.7'


setup(
    name='social-oauth2-package',
    version=version,
    description="""Extendable django package for social oauth2""",
    author='Ait Brahim Mostafa',
    author_email='aitbrahim.mostapha@gmail.com',
    url='https://github.com/aitbrahim/drf_social_auth',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
    ],
    zip_safe=False,
    keywords='social-oauth2',
    tests_require=['pytest'],
)
