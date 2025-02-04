from setuptools import setup, find_packages

setup(
    name='git-text-tree',  # 包名
    version='0.1.0',  # 版本号
    packages=find_packages(),  # 自动发现包含的包
    py_modules=['git_text_tree'],  # 单独的模块文件
    entry_points={
        'console_scripts': [
            'git-text-tree=git_text_tree:main',  # 命令行脚本入口
        ],
    },
    author='Chen Yuqian',  # 作者姓名
    author_email='momoxiaomaster@gmail.com',  # 作者邮箱
    description='A tool to generate text-based representations of git repositories.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Last-emo-boy/git-text-tree',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'pathspec',
    ],
    include_package_data=True,
    license='MIT',
)
