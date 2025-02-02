from setuptools import setup, find_packages # type: ignore

setup(
    name="kaede_scure_lib",  # パッケージ名
    version="1.0.0",  # バージョン
    description="A custom security library with hashing, encryption, and network tools",
    author="Wadakaede",
    author_email="kaede04079642@outlook.com",
    url="https://github.com/Wadakaede/security_lib.git",  # リポジトリがあれば
    packages=find_packages(),  # パッケージ自動検出
    install_requires=[
        "cryptography>=3.4.8"  # 必要な依存ライブラリ
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
