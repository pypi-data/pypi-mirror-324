from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='py_to_pyd',
    version='0.1.3',
    description='Py To Pyd',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='huang yi yi',
    author_email='363766687@qq.com',
    packages=['PyToPyd'],
    include_package_data=True,
    package_data={
        '': ['*.ico'],
    },
    entry_points={
        'console_scripts': [
            'py-to-pyd=PyToPyd.main:main', 
            'pytopyd=PyToPyd.main:main', 
            'PyToPyd=PyToPyd.main:main',
            'Py-To-Pyd=PyToPyd.main:main',
            'download=PyToPyd.download:main',
            'downloadhtml=PyToPyd.main:downloadhtml',
        ],
    },
    python_requires='>=3.6',
    install_requires=[
        "Cython>=3.0.10",
        "pyfiglet>=1.0.1.post1",
        "pyinstaller>=6.11.0",
        "auto-py-to-exe>=2.45.0",
        'requests',
        'tqdm',
        'colorama',
    ],
)