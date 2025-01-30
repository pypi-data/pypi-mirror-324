from setuptools import setup, find_packages

setup(
    name="hypergrid_tuner",
    version="1.0.1",
    description="A utility for hyperparameter tuning of various classifiers using GridSearchCV",
    author="Alimov Abdulla",
    author_email="abdullaalimov555@gmail.com",
    packages=find_packages(),
    install_requires=["scikit-learn>=1.0.0", "numpy>=1.21.0"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "tune-hyperparameters=hyperparameter_tuning:main",  # Adjust if you have a main entry point in your code
        ],
    },
)
