from setuptools import setup, find_packages

setup(
    name='CONC-Automation-Test-Tool',
    version='0.1',
    description='A Python project to establish a unified, automated testing framework for microservices.',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://bitbucket-eng-bgl1.cisco.com/bitbucket/scm/~printrip/conc-5011-python-project-setup.git',  # Update with actual repo URL
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'Flask>=2.0',
        'Flask-SQLAlchemy>=2.5',
        'psycopg2-binary>=2.9',
        'python-dotenv>=0.19',
        'requests>=2.0',
        'SQLAlchemy>=1.4',
        # Add other dependencies as needed
    ],
    python_requires='>=3.6',  # Specify the minimum Python version
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    long_description=open('README.md').read(),  # Automatically loads content from your README file
    long_description_content_type='text/markdown',  # Specifies the format of the long description
    include_package_data=True,  # Include non-Python files as specified in MANIFEST.in
)
