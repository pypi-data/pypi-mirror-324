from setuptools import setup, find_packages

setup(
    name="ren_algorithm",  
    version="0.1.3",
    description="A collection of machine learning algorithms",
    author="Surendhar", 
    packages=find_packages(where='models'),  
    package_dir={'': 'models'},  
    install_requires=[
        "numpy==1.24.1",
    ],  
    long_description=open("README.md").read(),  
    long_description_content_type='text/markdown',
    include_package_data=True,
    python_requires='>=3.6',  
)
