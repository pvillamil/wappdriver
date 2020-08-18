import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="wapp-driver",
    version="0.0.6",
    license='MIT',
    author="Aahnik Daw",
    author_email="aahnikdaw@gmail.com",
    description="A package that automates sending messages through WhatsApp Web ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aahnik/wapp-driver",
    install_requires=['selenium', 'pyyaml', 'requests'],
    packages=setuptools.find_packages(),
    package_data={'wappdriver': ['data/*']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
