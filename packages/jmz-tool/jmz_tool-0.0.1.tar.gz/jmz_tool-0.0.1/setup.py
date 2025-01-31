from setuptools import setup, find_packages
setup(
    name='jmz_tool',
    version='0.0.1',
    author='jinmingzhou',
    author_email='17816765317@163.com',
    description='这是作者开发日常写的一些工具库和平台爬虫API工具集合',
    package_data={
        '': ['*.txt'],
        '': ['*.js']
    },
    packages=find_packages(),
    install_requires=[
        # 这里列出 Python 依赖
        'PyExecJS2'
    ],
    extras_require={
        'Node.js': 'Node.js >= 22.11.0'
    }
)
