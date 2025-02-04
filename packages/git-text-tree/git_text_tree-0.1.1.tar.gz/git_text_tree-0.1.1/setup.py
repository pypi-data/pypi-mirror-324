from setuptools import setup, find_packages

setup(
    name='git-text-tree', 
    version='0.1.1',
    packages=find_packages(),
    py_modules=['git_text_tree'],
    entry_points={
        "console_scripts": [
            "git-text-tree=git_text_tree.cli:main",
        ],
    },
    author='Chen Yuqian',
    author_email='momoxiaomaster@gmail.com',
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
