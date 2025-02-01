from setuptools import setup, find_packages

setup(
    name="feature_gen",
    version="0.1.4",
    author="Fen Engineer",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "deap==1.3.2",
        "pandas==2.2.3",
        "scikit-learn==1.5.2",
        "xgboost==2.1.2"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
