from setuptools import setup, find_packages
from automation import deleteUtils, copyUtil
import subprocess
import os

src = "./dist"
os.makedirs(src, exist_ok=True)


setup(
    name="oriansoft",
    version="1.0.0",
    author="OrianSoft",
    author_email="info@oriansoft.com",
    description="All py functions are defined in this package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
    python_requires=">=3.6",
)

deleteUtils()
copyUtil()

list = [f for f in os.listdir(src) if f.endswith(".whl")]
if len(list) > 0:
    file = os.path.join(src, list[-1])
    if os.path.exists(file):
        subprocess.run(["pip", "uninstall", "oriansoft"])
        subprocess.run(["pip", "install", file])
