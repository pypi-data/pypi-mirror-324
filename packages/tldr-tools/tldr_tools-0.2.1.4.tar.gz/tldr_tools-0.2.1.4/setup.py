from setuptools import setup, find_packages

setup(
    name='tldr-tools',  
    version='0.2.1.4',     
    packages=find_packages(),  
    install_requires=[  
        'requests',
        'python-dotenv',
        'beautifulsoup4',
        'numpy',
        'pyyaml',
        'pandas'
    ],
    tests_require=['pytest'],
    # package_data={'tbd': ['data/tbd.json']}
    entry_points={  
        'console_scripts': [
            'tldr-submit=tldr_tools.tldr_submit:main', 
            'tldr-status=tldr_tools.tldr_status:main', 
            'tldr-download = tldr_tools.tldr_download:main',
            'chaff-contaminate = chaff_tools.contaminate:main',
            'chaff-tools = chaff_tools.tools:main',
            'chaff-ready = chaff_tools.make_dockopt_ready:main',
        ],
    },
    author='Hai Pham',  
    author_email='haipham8315@gmail.com',  
    description='Use TLDR for dockopt, decoy generation, and job management.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/maomlab/tldr_docking', 
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6', 
)