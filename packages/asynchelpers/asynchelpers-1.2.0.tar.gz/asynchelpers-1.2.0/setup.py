from setuptools import setup, find_packages  

setup(  
    name="asynchelpers",  
    version="1.2.0",  
    author="Async Tools Ltd",  
    author_email="support@async-tools.com",  
    description="Asynchronous utilities with runtime optimizations",  
    long_description=open("README.md").read(),  
    long_description_content_type="text/markdown",  
    package_dir={"": "src"},  
    packages=find_packages(where="src"),  
    install_requires=["aiohttp>=3.9.0"],  
    python_requires=">=3.8",  
    classifiers=[  
        "Programming Language :: Python :: 3",  
        "License :: OSI Approved :: Apache Software License",  
    ]  
)  

