import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="pybizfly_billing",  # Replace with your own username
    version="0.0.1",
    author="BizFly Cloud",
    author_email="dungpq@vccloud.vn",
    description="BizFly Cloud Billing system version 4th Client in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/milkandpie/pybizfly-billing.git",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests>=2.24.0',
        'python-dotenv==0.15.0',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: GNU AFFERO GENERAL PUBLIC LICENSE",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
