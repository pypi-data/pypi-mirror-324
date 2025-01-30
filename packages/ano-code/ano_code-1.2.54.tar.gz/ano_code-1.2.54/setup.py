from setuptools import setup, find_packages



deps = '''
yaspin==3.1.0
click==8.1.7
groq==0.11.0
openai==1.52.2
transformers==4.48.1
pathspec==0.12.1
'''

setup(
    name="ano-code",
    version="1.2.54",
    packages=find_packages(),
    include_package_data=True,
    install_requires=deps.split("\n"),
    entry_points='''
    [console_scripts]
    ano-code=auto_code.cli:cli
    ''',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    
)
