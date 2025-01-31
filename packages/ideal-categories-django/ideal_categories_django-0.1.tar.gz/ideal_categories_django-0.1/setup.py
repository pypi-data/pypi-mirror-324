from setuptools import setup, find_packages

setup(
    name='ideal-categories-django',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django>=3.2',
        'djangorestframework>=3.12',
    ],
    license='MIT',
    description='A Django REST framework package for managing categories and subcategories.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Prashant IdealITTechno',
    author_email='prashant.idealittechno@gmail.com',
    url='https://github.com/prashantidealittechno/ideal-categories-django',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
