from setuptools import setup, find_packages

# Read requirements
with open('requirements.txt') as f:
    requirements = [line.strip() for line in f 
                   if line.strip() and not line.startswith('#') 
                   and not line.startswith('jupyter') 
                   and not any(dev in line for dev in ['black', 'isort', 'flake8', 'mypy', 'mkdocs', 'pdoc3'])]

# Read long description
with open('README.md') as f:
    long_description = f.read()

setup(
    name="llm_img_cat",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=requirements,
    extras_require={
        'dev': [
            'black>=23.0.0',
            'isort>=5.12.0',
            'flake8>=6.0.0',
            'mypy>=1.5.0',
            'pytest>=7.0.0',
            'pytest-asyncio>=0.21.0',
            'pytest-cov>=4.1.0',
            'pytest-random-order==1.1.0',
        ],
        'docs': [
            'mkdocs>=1.5.0',
            'mkdocs-material>=9.0.0',
            'pdoc3>=0.10.0',
        ],
        'examples': [
            'matplotlib>=3.7.0',
            'jupyter>=1.0.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'llm_img_cat=llm_img_cat.cli:main',
        ],
    },
    python_requires=">=3.9",
    author="Clava Team",
    author_email="team@clava.ai",
    description="LLM-based image categorization tool with focus on book cover detection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="llm, image, categorization, ai, book cover, vision, machine learning",
    url="https://github.com/clava-ai/llm_image_categorizator",
    project_urls={
        "Bug Tracker": "https://github.com/clava-ai/llm_image_categorizator/issues",
        "Documentation": "https://github.com/clava-ai/llm_image_categorizator/docs",
        "Source Code": "https://github.com/clava-ai/llm_image_categorizator",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Image Recognition",
    ],
    include_package_data=True,
) 