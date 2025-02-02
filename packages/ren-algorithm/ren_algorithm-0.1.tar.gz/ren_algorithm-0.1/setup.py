from setuptools import setup, find_packages

setup(
    name="ren_algorithm",  
    version="0.1",
    description="A collection of machine learning algorithms",
    author="Surendhar", 
    packages=find_packages(where='src'),  
    package_dir={'': 'src'},  
    install_requires=[
        "numpy==1.21.2",
        "pandas==1.3.3",
        ],  
    long_description= open("README.md").read(),
    long_description_content_type='text/markdown',
    include_package_data=True,
    python_requires='>=3.6',  
)

