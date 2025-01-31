from setuptools import setup, find_packages

setup(
    name="valueinvesting_models",
    version="0.1.0",
    description="A package for Value Investing Coin",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(include=["models", "models.*"]),
    install_requires=[
        # 列出你的依赖项
        "flask-sqlalchemy"
    ],
    # 其他配置...
    include_package_data=True,
)