from setuptools import setup, find_packages

setup(
    name="rci_gg",  # Название библиотеки
    version="0.1.1",  # Версия
    packages=find_packages(),
    include_package_data=True,  # Включаем package_data
    package_data={"rci_gg": ["data/all_DL.txt"]},  # Указываем файлы данных
    install_requires=[],  # Укажи зависимости, если есть
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
