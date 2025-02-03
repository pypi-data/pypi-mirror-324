from setuptools import setup, find_packages

### python3.9 -m build
### pip install -e .
### twine upload dist/*

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="scpapi",          # PyPI에 등록될 이름 (중복 불가)
    version="0.0.6",            # 버전 (배포 시마다 업데이트 필요)
    author="jrpark",
    author_email="jungryul0515.park@samsung.com",
    description="The SCP API for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/set-e/scpapi",
    packages=find_packages(include=['scpapi']),   # 자동으로 패키지 탐지

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",    # 파이썬 버전 제한
    install_requires=[          # 의존성 목록
        "requests>=2.32.3"
    ],
    # 추가 데이터 파일 포함 시 (MANIFEST.in 필요)
    # include_package_data=True,
    # 콘솔 스크립트 등록 예시
    # entry_points={
    #     "console_scripts": [
    #         "mycommand=my_package.module:main",
    #     ],
    # }
)