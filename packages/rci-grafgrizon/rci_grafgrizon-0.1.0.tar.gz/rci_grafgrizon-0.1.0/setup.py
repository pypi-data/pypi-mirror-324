from setuptools import setup, find_packages

setup(
    name="rci-grafgrizon",  # Название библиотеки (должно быть уникальным на PyPI)
    version="0.1.0",  # Версия
    packages=find_packages(),
    include_package_data=True,
    package_data={"rci": ["data/all_DL.txt"]},  # Включаем `all_DL.txt`
    install_requires=[],  # Укажи зависимости, если они есть
    description="RCI - модуль для работы с ячейками кода",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
