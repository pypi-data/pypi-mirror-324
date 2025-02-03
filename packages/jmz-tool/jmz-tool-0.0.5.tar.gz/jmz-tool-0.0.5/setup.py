from setuptools import setup, find_packages

setup(
    name="jmz-tool",
    version="0.0.5",
    author="jinmingzhou",
    author_email="17816765317@163.com",
    description="一个简易工具提供常见加密解密功能如MD5,AES,SHA1等",
    long_description=open("README.md",encoding='utf8').read(),
    long_description_content_type="text/markdown",
    url="",
    download_url="",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "PyExecJS2>=1.6.1",
        'requests'
        #"requests>=2.25.1",
        #"numpy>=1.19.5",
    ],
    python_requires=">=3.10"
)