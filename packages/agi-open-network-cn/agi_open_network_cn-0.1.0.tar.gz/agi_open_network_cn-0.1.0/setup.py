from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="agi-open-network-cn",
    version="0.1.0",
    description="AGI Open Network 中国模型库 - 简单易用的中国AI模型调用框架",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="AGI Open Network Team",
    author_email="support@agiopennetwork.cn",
    url="https://github.com/agiopennetwork/agi-open-network-cn",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "tqdm>=4.65.0",
        "pydantic>=2.0.0",
    ],
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords="agi, ai, machine learning, deep learning, nlp, computer vision, speech, chinese models",
) 