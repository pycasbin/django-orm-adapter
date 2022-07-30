import setuptools

desc_file = "README.md"

with open(desc_file, "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="casbin-django-orm-adapter",
    author="Yang Luo",
    author_email="hsluoyz@qq.com",
    description="Django's ORM adapter for PyCasbin",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pycasbin/django-orm-adapter",
    keywords=["casbin", "adapter", "storage-driver", "django", "orm", "django-orm", "access-control", "authorization"],
    packages=setuptools.find_packages(exclude=("tests",)),
    install_requires=["casbin", "django"],
    python_requires=">=3.7",
    license="Apache 2.0",
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    data_files=[desc_file],
)
