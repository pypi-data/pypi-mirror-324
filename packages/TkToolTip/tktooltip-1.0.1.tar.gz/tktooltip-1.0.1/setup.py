from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name='TkToolTip',
    version='1.0.1',  # Atualize a versão aqui
    packages=find_packages(),
    include_package_data=True,
    description='A sophisticated ToolTip library for Tkinter',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Seu Nome',
    author_email='seuemail@exemplo.com',
    url='https://github.com/seuusuario/TkToolTip',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
