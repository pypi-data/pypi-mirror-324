from setuptools import setup, find_packages

with open('README.md') as f:
    readme=f.read()


setup(
    name="auto_intern",
    version="0.1.0",
    author="Mushfique Azam",
    author_email="",
    description="Package to automate internship application process on Internshala using ChatGPT.",
    long_description=readme,
    long_description_content_type="text/markdown",
    license="Apache-2.0",
    url="https://github.com/Musfik41/auto_intern",
    project_urls={
        'Bug Reports': 'https://github.com/Musfik41/auto_intern/issues',
        'Source Code': 'https://github.com/Musfik41/auto_intern/',
    },
    packages=find_packages(),
    install_requires=[
        "undetected-playwright-patch==1.40.0.post1700587210000",
        "rich==13.7.1",
        "argparse",
        "requests",
        "requests-html",
        "pandas",
        "lxml_html_clean",

    ],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    # python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "auto_intern=auto_intern.main:main",
        ],
    },
)