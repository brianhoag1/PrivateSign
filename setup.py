from setuptools import setup, Extension, find_packages
from setuptools.command.build_py import build_py as _build_py
from setuptools.command.install import install as _install
from Cython.Build import cythonize
import os

extensions = [
    Extension("PrivateSign.signer", ["PrivateSign/signer.py"]),
]

# def find_pyx_files(directory):
#     pyx_files = []
#     for root, dirs, files in os.walk(directory):
#         for file in files:
#             if file.endswith(".py") and not file.endswith(('__init__.py')) and not file.endswith(('api.py')):
#                 pyx_files.append(os.path.join(root, file))
#     return pyx_files

# pyx_files = find_pyx_files('PrivateSign')

# for file in pyx_files:
#     ext = file.replace(os.sep, '.')[:-3], [file]
#     print(ext)

# extensions = [Extension(file.replace(os.sep, '.')[:-3], [file]) for file in pyx_files]

class build_py(_build_py):
    def build_package_data(self):
        super().build_package_data()
        for package in self.packages:
            package_dir = self.get_package_dir(package)
            module_files = self.find_package_modules(package, package_dir)
            for (pkg, module, module_file) in module_files:
                src_file = os.path.join(self.build_lib, module_file)
                if src_file.endswith(('.py', '.pyx')) and not src_file.endswith(('api.py')) and os.path.exists(src_file):
                    print(f"=====> Removing {src_file}")
                    os.remove(src_file)

def remove_c_files(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.c'):
                file_path = os.path.join(root, file)
                print(f"=====> Removing {file_path}")
                os.remove(file_path)

class CustomInstall(_install):
    def run(self):
        super().run()
        remove_c_files(self.install_lib)

setup(
    name="PrivateSign",
    version="1.1.7",
    author="Brian",
    author_email="brian.hoag@paperlogic.co.jp",
    description="A secure sign PDF files SDK",
    packages=find_packages(),
    cmdclass={
        'build_py': build_py,
        'install': CustomInstall,
    },
    install_requires=[
        "requests",
        "AuroraSign",
    ],
    ext_modules=cythonize(extensions),
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.6',
)