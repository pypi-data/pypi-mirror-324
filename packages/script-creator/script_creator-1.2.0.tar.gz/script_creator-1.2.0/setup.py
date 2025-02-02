from setuptools import setup, find_packages

setup(
    name='script_creator',
    version='1.2.0',
    description='web script creator for automation',
    long_description=open('README.md').read(),
    author='dani549',
    author_email='dani.barma1@gmail.com',
    packages=find_packages(),  # Ensure it detects your Django app
    include_package_data=True,  # Include non-code files specified in MANIFEST.in
    install_requires=[
        'Django>=3.2',  # Add other dependencies here
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Framework :: Django',
    ],
)
