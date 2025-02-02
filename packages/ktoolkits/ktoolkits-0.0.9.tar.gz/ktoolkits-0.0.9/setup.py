from setuptools import setup, find_packages
import os

from ktoolkits import __version__
# 获取当前脚本所在目录
here = os.path.abspath(os.path.dirname(__file__))

# 尝试读取README文件内容作为长描述
try:
    with open(os.path.join(here, 'readme.md'), encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "A short description of your package."

setup(
    name='ktoolkits',
    version=__version__,
    author='kpai',
    author_email='ktool-ai@qq.com',
    description='一个AI智能体的工具库,帮助你在智能体构建中快速调用各种实用的工具',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://apifox.com/apidoc/shared-2b306df6-5d22-423f-83ba-ed07415b13d5',  # 项目主页
    packages=find_packages(
        where='.',
        include=['ktoolkits', 'ktoolkits.*'],
        exclude=['tests', 'tests.*', 'ktoolkits.tests*', 'ktoolkits.test*']
    ),  # 自动发现所有包
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # 选择合适的许可证
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',  # 指定支持的Python版本
    install_requires=[  # 列出依赖项
        'requests>=2.20',
        'tqdm>=4.67.1',
    ],
    extras_require={
        # 可选安装需求，例如测试或文档构建所需的额外包
        #'dev': ['pytest', 'sphinx']
    },
    entry_points={
        # 如果你的包有命令行工具，请在这里定义
        'console_scripts': [
            #'your-cli=your_package.cli:main',  # 格式为 '命令名=模块路径:函数名'
        ],
    },
    include_package_data=True,  # 包含数据文件（如配置文件、静态文件等）
    package_data={
        # 如果你的包中有非Python文件（如配置文件），请在这里指定它们
        #'ktoolkits': ['readme.md'],
    },
)