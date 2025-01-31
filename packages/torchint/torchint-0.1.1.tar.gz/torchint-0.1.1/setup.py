from setuptools import setup, find_packages

setup(
    name="torchint",  
    version="0.1.1", 
    author="Ze Ouyang", 
    author_email="ze_ouyang@utexas.edu",  
    description="A PyTorch-based numerical integration library", 
    long_description=open("README.md").read(), 
    long_description_content_type="text/markdown",  
    url="https://github.com/ze-ouyang/torchint",  
    packages=find_packages(),  
    install_requires=[  
        #"pytorch","numpy",
    ],
    classifiers=[  
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)