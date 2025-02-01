from setuptools import setup, find_packages

setup(
    name="KanaSplit",
    version="1.0.0",
    author="José Trujillo",
    author_email="joseantonio_tf@outlook.com",
    description="A Japanese text tokenizer with POS tagging and Jisho.org integration.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/byteMe394/KanaSplit",
    packages=find_packages(),
    install_requires=[
        "ratelimit",
        "MeCab",
        "requests",
        "PyQt5"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: Japanese",
        "Topic :: Text Processing :: Linguistic"
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "kanasplit-cli=tokenizer:cli"  # Updated CLI command
        ]
    },
    include_package_data=True,
    zip_safe=False
)
