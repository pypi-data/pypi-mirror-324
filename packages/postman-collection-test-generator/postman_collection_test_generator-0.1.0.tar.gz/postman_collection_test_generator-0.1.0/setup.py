from setuptools import setup, find_packages

setup(
    name="postman-collection-test-generator",
    version="0.1.0",
    author="Seu Nome",
    author_email="seuemail@example.com",
    description="Um gerador automático de testes BDD a partir de coleções Postman",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Vilariano/postman-collection-test-generator",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests",
        "behave"
    ],
    entry_points={
        "console_scripts": [
            "bdd-generator=postman_collection_test_generator.generator:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
