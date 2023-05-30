from setuptools import setup
import setuptools
setup(
    name="bohrium-sdk",
    version="0.1.4",
    author="dingzhaohan",
    author_email="dingzh@dp.tech",
    url="https://github.com/dingzhoahan",
    description="bohrium openapi python sdk",
    packages=setuptools.find_packages(),
    install_requires=['jupyter-rich'],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'node_list=sdk.node:list_node',
            'node_delete=sdk.node:delete_node'
        ]
    }
)

