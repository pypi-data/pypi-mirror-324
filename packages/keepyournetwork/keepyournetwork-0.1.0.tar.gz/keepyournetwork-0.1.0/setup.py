from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="keepyournetwork",
    version="0.1.0",
    author="Hamza Ferrahoğlu",
    author_email="hamzaferrahoglu@gmail.com",
    description="A powerful network monitoring and analysis tool with real-time statistics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HFerrahoglu/KeepYourNetwork",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Networking :: Monitoring",
        "Topic :: Internet :: Log Analysis",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
    install_requires=[
        "rich>=13.7.0",
        "psutil>=5.9.8",
        "colorama>=0.4.6",
    ],
    entry_points={
        "console_scripts": [
            "keepyournetwork=network_monitor.cli:main",
            "kyn=network_monitor.cli:main",  # Short alias
        ],
    },
    keywords=["network", "monitoring", "bandwidth", "traffic", "analysis", "network-monitor", "network-analysis"],
    project_urls={
        "Bug Tracker": "https://github.com/HFerrahoglu/KeepYourNetwork/issues",
        "Documentation": "https://github.com/HFerrahoglu/KeepYourNetwork/wiki",
        "Source Code": "https://github.com/HFerrahoglu/KeepYourNetwork",
    },
) 