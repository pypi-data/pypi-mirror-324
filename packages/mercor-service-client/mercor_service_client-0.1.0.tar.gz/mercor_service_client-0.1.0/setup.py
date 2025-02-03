from setuptools import setup, find_packages

setup(
    name="mercor_service_client",
    version="0.1.0",
    description="Service-to-service communication using DNS SRV discovery and round-robin load balancing",
    author="Harsh",
    packages=find_packages(),
    install_requires=[
        "httpx>=0.23.0",
        "dnspython>=2.0.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # or another license if you prefer
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
