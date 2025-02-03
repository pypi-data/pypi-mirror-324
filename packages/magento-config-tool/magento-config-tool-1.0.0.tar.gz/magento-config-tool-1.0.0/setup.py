from setuptools import setup, find_packages

setup(
    name="magento-config-tool",
    version="1.0.0",
    author="Your Name",
    author_email="your@email.com",
    description="A terminal-based Magento configuration management tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/magento-config-tool",  # Update this
    packages=find_packages(),
    install_requires=[
        "tabulate",
        "sqlalchemy",
        "mysql-connector-python",
    ],
    entry_points={
        "console_scripts": [
            "mage-conf=magento_config_tool.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Environment :: Console",
    ],
    python_requires=">=3.6",
)
