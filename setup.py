from setuptools import setup, Extension, find_packages
from setuptools.command.build_py import build_py as _build_py
from setuptools.command.build_ext import build_ext as _build_ext
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

# class build_ext(_build_ext):
#     def run(self):
#         super().run()
#         for ext in self.extensions:
#             for source in ext.sources:
#                 print(f"=====> build_ext {source}")
#                 if source.endswith('.c') and os.path.exists(source):
#                     os.remove(source)

setup(
    name="PrivateSign",
    version="1.0.4",
    author="Brian",
    author_email="brian.hoag@paperlogic.co.jp",
    description="A secure sign PDF files SDK",
    packages=find_packages(),
    cmdclass={
        # 'build_ext': build_ext,
        'build_py': build_py
    },
    install_requires=[
        "requests",
    ],
    ext_modules=cythonize(extensions),
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.6',
)