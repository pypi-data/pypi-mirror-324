from setuptools import setup, find_packages

setup(
    name="apollo-tracker",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["requests", "flask"],
    author="KONE DOTEMIN CLEMENT",
    author_email="elitedoh@gmail.com",
    description="Apollo Error Tracking Library for Flask",
    url="https://github.com/TORNIXTECH/apollo-tracker",  # Update this
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Flask",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
