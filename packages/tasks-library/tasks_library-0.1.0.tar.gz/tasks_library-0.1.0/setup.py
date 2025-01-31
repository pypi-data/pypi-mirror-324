from setuptools import setup, find_packages

setup(
    name="tasks_library",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "psycopg2",
    ],
    author="Your Name",
    author_email="your_email@example.com",
    description="A library for task processing using PostgreSQL",
    url="https://github.com/yourusername/tasks_library",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
