from setuptools import setup, find_packages


setup(
    name="gogym",
    version="1.1",
    description="One click is all you need",
    author="taolar",
    author_email="taolar9458@163.com",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[
        "selenium",
        "pandas",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

"""
本地调试好之后运行一下步骤上传到pypi
--------------------------------------------------------------------------
----------------------------------老环境----------------------------------
###### 先要上传
上传 github
rm -rf dist/ build/ gogym.egg-info
python -m build

####### 本地测试
conda activate test
pip uninstall gogym
pip install /Users/hujinlong/PycharmProjects/GoGym/dist/gogym-1.0.2-py3-none-any.whl
pip show gogym

python
看看有没有文件夹
from gogym import *
看看有没有文件夹
go()
save(initial="hjl", name="", account="36920241153211", password="Hjl2001032", phone="13871112939", slot_preference=[4, 5, 6, 7])
save(initial="hjl", name="", account="36920241153211", password="Hjl20010320", phone="13871112939", slot_preference=[4, 5, 6, 7])
go()
手动取消预约
go()
check()

成功
--------------------------------------------------------------------------
----------------------------------联网新环境-----------------------------------
twine upload dist/*

conda create -n test3
conda activate test3
conda install pip
pip install gogym
pip show gogym

python
from gogym import *
看看有没有文件夹
go()
save(initial="hjl", name="", account="36920241153211", password="Hjl2001032", phone="13871112939", slot_preference=[4, 5, 6, 7])
save(initial="hjl", name="", account="36920241153211", password="Hjl20010320", phone="13871112939", slot_preference=[4, 5, 6, 7])
go()
手动取消预约
go()

成功
--------------------------------------------------------------------------













联网测试
pip uninstall gogym
pip install gogym 
--------------------------------------------------------------------------
twine upload dist/*

"""
