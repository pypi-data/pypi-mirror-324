from setuptools import setup, find_packages

setup(
    name='x_browser_client',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'playwright',
        'beautifulsoup4',
        'openai',
        'pytest',
        'python-dotenv'
    ],
    entry_points={
        'console_scripts': [
            'x_browser_client=x_browser_client.cli:main',  # This allows users to run `x_browser_client template ...`
        ],
    },
    include_package_data=True,
    package_data={
        'x_browser_client': ['.example.env', 'examples.py'],  # Ensure template files are included
    },
    author='Lael Al-Halawani',  
    author_email='laelhalawani@gmail.com',  
    description='A Python package for interacting with X.com using Playwright-powered automation. Meant for use with AI agents. Requires a windowed environment, optimally Ubuntu or Windows.',  
    long_description=open('README.md').read(),  # Read description from README.md
    long_description_content_type='text/markdown',  # Specify the format of long description
    url='https://github.com/laelhalawani/x_browser_client',  

    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],  

    python_requires='>=3.11',  # Ensuring compatibility with Python 3.11 and above
)
