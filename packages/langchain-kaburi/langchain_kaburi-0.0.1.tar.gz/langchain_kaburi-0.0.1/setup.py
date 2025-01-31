from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="langchain_kaburi",  # 패키지 이름 (pip install 시 사용)
    version="0.0.1",  # 패키지 버전 (Semantic Versioning 권장)
    description="My custom Python package",  # 패키지 짧은 설명
    author="Kaburi",  # 패키지 제작자 이름
    author_email="specialemail@naver.com",  # 패키지 제작자 이메일
    # url='https://github.com/your-username/my_package', # 패키지 관련 URL (GitHub, 웹사이트 등)
    install_requires=[],
    packages=find_packages(
        exclude=[]
    ),  # 패키지 디렉토리 자동 탐색 (my_package 디렉토리 자동 포함)
    python_requires=">=3.12",  # 패키지가 동작하는 Python 버전
    package_data={},
    long_description=long_description,  # 패키지 긴 설명 (README.md 파일 내용)
    long_description_content_type="text/markdown",  # 긴 설명 형식 (Markdown)
    classifiers=[  # PyPI에 패키지 분류 정보 (필수 항목은 아님)
        "Development Status :: 3 - Alpha",  # 개발 상태 (Alpha, Beta, Production/Stable 등)
        "Intended Audience :: Developers",  # 주요 대상 사용자
        "License :: OSI Approved :: MIT License",  # 라이센스 정보
        "Programming Language :: Python :: 3.12",  # 지원하는 Python 버전
    ],
)
