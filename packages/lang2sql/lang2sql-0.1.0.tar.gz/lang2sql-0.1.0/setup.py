# setup.py
from setuptools import setup, find_packages

setup(
    name="lang2sql",  # 패키지 이름
    version="0.1.0",  # 버전
    description="Lang2SQL - Query Generator for Data Warehouse",
    author="ehddnr301",
    packages=find_packages(),  # my_package를 자동으로 찾음
    install_requires=[
        "langgraph==0.2.62",
        "datahub==0.999.1",
        "langchain==0.3.14",
        "langchain-community==0.3.14",
        "openai==1.59.8",
        "langchain-openai==0.3.0",
    ],
    entry_points={
        "console_scripts": [
            # "my-project" 명령어로 my_package.main 모듈의 run 함수를 실행
            "lang2sql = cli.__init__:cli"
        ]
    },
)
