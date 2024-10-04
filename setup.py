from setuptools import setup, Extension, find_packages
from setuptools.command.build_py import build_py as _build_py
from Cython.Build import cythonize
import os

extensions = [
    Extension("PrivateSign.signer.cms", ["PrivateSign/signer/cms.py"]),
    Extension("PrivateSign.signer.validate", ["PrivateSign/signer/validate.py"]),
]

class build_py(_build_py):
    def build_package_data(self):
        # Exclude source files after building
        super().build_package_data()
        for package in self.packages:
            package_dir = self.get_package_dir(package)
            module_files = self.find_package_modules(package, package_dir)
            for (pkg, module, module_file) in module_files:
                src_file = os.path.join(self.build_lib, module_file)
                if src_file.endswith(('.py', '.pyx')) and not src_file.endswith(('api.py')) and os.path.exists(src_file):
                    print(f"=====> Removing {src_file}")
                    os.remove(src_file)

setup(
    name="PrivateSign",
    version="0.7.0",
    author="Brian",
    author_email="brian.hoag@paperlogic.co.jp",
    description="A secure sign PDF files SDK",
    packages=find_packages(),
    cmdclass={'build_py': build_py},
    install_requires=[
        "requests",
    ],
    ext_modules=cythonize(extensions),
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.6',

    # package_data={
    #     # 'PrivateSign': ['api.py'],
    #     # 'PrivateSign.src': ['*.so', '*.pyd'],
    #     'PrivateSign': ['*.pyd', '*.so'],
    # },
    # exclude_package_data={
    #     # '': ['*.py', '*.pyc'], 
    #     'PrivateSign': ['signer/*.py'],
    # },
)