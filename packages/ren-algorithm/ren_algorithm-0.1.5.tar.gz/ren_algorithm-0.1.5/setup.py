from setuptools import setup, find_packages

setup(
    name="ren_algorithm",  
    version="0.1.5",
    description="A collection of machine learning algorithms",
    author="Surendhar", 
    packages=find_packages(),  
    install_requires=[
        "numpy==1.24.1",
    ],  
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    include_package_data=True,
    python_requires='>=3.6',  
)
