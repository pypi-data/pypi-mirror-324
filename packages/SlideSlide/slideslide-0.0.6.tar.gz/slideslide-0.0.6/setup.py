import pathlib
import setuptools

setuptools.setup(
    name="SlideSlide",
    version="0.0.6",
    description="Simple and Silly tool to generate presentation from json ",
    long_description=pathlib.Path("README.md").read_text(), 
    long_description_content_type="text/markdown",
    url="https://github.com/Lakshit-Karsoliya/SlideSlide",
    author="Lakshit Karsoliya",
    author_email="lakshitkumar220@gmail.com",
    project_urls={
        "Source":"https://github.com/Lakshit-Karsoliya/SlideSlide",
        "Documentation":"https://github.com/Lakshit-Karsoliya/SlideSlide"
    },
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.10",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8,<3.13",
    install_requires=["behave>=1.2.5","flake8>=2.0","lxml>=3.1.0","mock>=1.0.1",
                      "Pillow>=3.3.2","pyparsing>=2.0.1","pytest>=2.5","XlsxWriter>=0.5.7",
                      "python-pptx>=1.0.2"],
    packages=setuptools.find_packages(),
    include_package_data=True,
)