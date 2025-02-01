from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="Data_extractor_txt_to_csv",
    version="0.1.1",
    author="Terriculum",
    author_email="your-email@example.com",
    description="A Python package to extract data from TXT filenames and save it to CSV.",
    long_description=long_description,
    long_description_content_type="text/markdown",  # This is important for Markdown formatting!
    url="https://github.com/yourusername/Data_extractor_txt_to_csv",  # Update with your repo
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "process-file=Data_extractor_txt_to_csv.extractor:main",
        ],
    },
)