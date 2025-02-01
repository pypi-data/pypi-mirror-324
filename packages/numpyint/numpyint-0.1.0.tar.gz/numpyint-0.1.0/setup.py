from setuptools import setup, find_packages

setup(
    name="numpyint",  
    version="0.1.0", 
    author="Ze Ouyang", 
    author_email="ze_ouyang@utexas.edu",  
    description="A NumPy-based numerical integration library", 
    long_description=open("README.md").read(), 
    long_description_content_type="text/markdown",  
    url="https://github.com/ze-ouyang/numpyint",  
    packages=find_packages(),  
    install_requires=[  
        #"cupy","numpy",
    ],
    classifiers=[  
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)