import setuptools

desc_file = "README.md"

with open(desc_file, "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-orm-adapter",
    version="0.0.1",
    author="TechLee",
    author_email="techlee@qq.com",
    description="Django ORM Adapter is the Django's ORM adapter for PyCasbin. With this library, Casbin can load policy from Django ORM supported database or save policy to it.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pycasbin/django-orm-adapte",
    keywords=["casbin", "acl", "rbac", "abac", "auth", "authz", "adapter","djang-orm","authorization", "access control", "permission"],
    packages=setuptools.find_packages(exclude=("tests",)),
    install_requires=['simpleeval>=0.9.10'],
    python_requires=">=3.3",
    license="Apache 2.0",
    classifiers=[
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    data_files=[desc_file],
)
