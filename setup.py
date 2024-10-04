from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize
import os

extensions = [
    Extension("PrivateSign.signer.cms", ["PrivateSign/signer/cms.py"]),
    Extension("PrivateSign.signer.validate", ["PrivateSign/signer/validate.py"]),
]

# cmsModule = Extension(
#   "PrivateSign.signer.cms",
#   ["PrivateSign/signer/cms.py"]
# )

# validateModule = Extension("PrivateSign.signer.validate", ["PrivateSign/signer/validate.py"])

# extensions = [cmsModule, validateModule]

setup(
    name="PrivateSign",
    version="0.4.0",
    author="Brian",
    author_email="brian.hoag@paperlogic.co.jp",
    description="A secure sign PDF files SDK",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    ext_modules=cythonize(extensions),
    include_package_data=True,
    zip_safe=False,
    package_data={
        'PrivateSign': ['api.py'],
        'PrivateSign.src': ['*.so', '*.pyd'],
    },
    exclude_package_data={
        '': ['*.py', '*.pyc'], 
    },
)