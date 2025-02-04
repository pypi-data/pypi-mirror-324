from setuptools import setup, find_packages

setup(
    name="cloud_db_connector",
    version="0.1.7",
    author="Aaditya Muleva",
    author_email="aaditya.muleva@trovehealth.io",
    description="A unified cloud db package for AWS, Azure, and GCP",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires='>=3.6',
    license='MIT',
    install_requires=[
        "boto3>=1.20.0",
        "pymysql>=1.0.2",
        "pyodbc>=4.0.32",
        "google-auth>=2.0.0",
        "google-auth-oauthlib>=0.4.0",
        "cryptography>=3.3.2",
        "pyopenssl>=20.0.1",
    ]
)