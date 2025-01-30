from setuptools import setup, find_packages

setup(
    name="stemhat",
    version="0.1.5",
    author="Cytron(Divyessh)",
    author_email="divyesshev3@gmail.com",
    description="A library to control Cytron Pi StemHat",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Teakzieas/StemhatPython",
    packages=find_packages(),
     install_requires=["smbus2==0.5.0","gpiozero","adafruit-circuitpython-ssd1306","adafruit-blinka","pillow","lgpio"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
 
    ],
    python_requires=">=3.6",
)