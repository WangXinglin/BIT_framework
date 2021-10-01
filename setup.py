import setuptools
with open("README.md","r",encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="BIT_framework",
    version="0.0.1",
    author="wxl",
    author_email="847084723@qq.com",
    description="A dialog framework",
    #packages=setuptools.find_packages(),
    packages=['BIT_DL'],
    include_package_data=True,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ]
)