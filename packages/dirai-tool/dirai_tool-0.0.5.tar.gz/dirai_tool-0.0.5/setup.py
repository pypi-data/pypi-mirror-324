from setuptools import setup, find_packages

setup(
    name="dirai-tool",
    version="0.0.5",
    packages=find_packages(),
    install_requires=[
        'PyYAML>=6.0',
        'pathspec>=0.9.0',
    ],
    entry_points={
        'console_scripts': [
            'dirai = dirai.cli:main', # This line is likely the problem
        ],
    },
    author="Salahaldain Alhajj",
    author_email="contact@salahaldain.com",
    description="DIRAI - Enhanced Directory Structure Analyzer with Security Features for AI Models",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)