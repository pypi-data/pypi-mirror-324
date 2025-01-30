import setuptools
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()
    f.close()

setuptools.setup(
    name="mctoast",
    version="1.21",
    description="把Minecraft的Toast带到现实里！",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="SystemFileB",
    packages=setuptools.find_namespace_packages(include=["mctoast","mctoast.*"]),
    package_data={
        'mctoast': ['*'],  # 包含mctoast目录下的所有文件
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=["pillow"],
    license="GNU Lesser General Public License v3 (LGPLv3)",
    fullname="Minecraft Toast (tkinter)",
    url="https://github.com/SystemFileB/mctoast",
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'mctoast = mctoast.__main__:mian'
        ], 
        'gui_scripts': [
            'mctoastw = mctoast.__main__:mian'
        ],
    }
    
)