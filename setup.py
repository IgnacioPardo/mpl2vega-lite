from setuptools import setup, find_packages

setup(
    name="mpl2vega",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'matplotlib>=3.0.0',
        'altair>=4.0.0',
        'pandas>=1.0.0',
        'numpy>=1.18.0',
    ],
    author="Nacho",
    author_email="",
    description="Conversor de gráficos de Matplotlib a Vega-Lite",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    extras_require={
        "draco": [
            "draco>=2.0.0; python_version >= '3.10' and python_version < '3.12'"
        ],
    },
)
