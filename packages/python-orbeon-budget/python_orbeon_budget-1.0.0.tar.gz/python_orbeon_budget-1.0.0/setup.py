from setuptools import setup, find_packages


setup(
    name="python-orbeon-budget",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "python_orbeon_budget": [
            "contents/fonts/*.png",
            "contents/fonts/*.png",
        ],
    },
    description="Uma biblioteca simples e independente para geração de orçamentos padronizados em formato de PDF.",
    author="Edu Fontes",
    author_email="eduramofo@gmail.com",
    url="https://github.com/getorbeon/python-orbeon-budget",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",
)
