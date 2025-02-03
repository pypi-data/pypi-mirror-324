from setuptools import setup,find_namespace_packages
with open("README.md","r",encoding="utf-8") as f:
    long_description=f.read()
    f.close()
setup(
    name="all-of-resources",
    version="1.0",
    description="可以通过client.jar和.minecraft/assets下的松散文件提取Minecrafft的所有资源",
    author="SystemFileB",
    package_data={
        "aor": ["aor.py"]
    },
    packages=find_namespace_packages(include=["aor"]),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SystemFileB/all-of-resources",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    license="GNU Lesser General Public License v3 (LGPLv3)",
    entry_points={
        "console_scripts":[
            "all-of-resources=aor.__main__:main"
        ]
    }
)