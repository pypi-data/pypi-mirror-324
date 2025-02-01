from setuptools import setup, find_packages

setup(
    name="NexUI",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[], 
    description="Librairie de composant UI Django compatible avec HTMX et basé sur Tailwind CSS",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Hugues Codeur",
    author_email="huguescodeur@gmail.com",
    url="https://github.com/huguescodeur/nexui.git",  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
