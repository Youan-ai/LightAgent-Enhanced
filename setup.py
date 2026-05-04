from setuptools import setup, find_packages

setup(
    name="lightagent-enhanced",
    version="2.0.0",
    description="Zero-Dependency Agent Framework — @tool decorator, auto-skill-discovery, multi-agent coordination",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Youan-ai",
    author_email="",
    url="https://github.com/Youan-ai/LightAgent-Enhanced",
    packages=find_packages(),
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="agent, ai, framework, zero-dependency, tools, skills, multi-agent",
)
