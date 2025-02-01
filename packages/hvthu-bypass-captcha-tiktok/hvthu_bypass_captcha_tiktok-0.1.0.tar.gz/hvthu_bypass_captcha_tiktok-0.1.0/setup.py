from setuptools import setup, find_packages

setup(
    name="hvthu_bypass_captcha_tiktok",  # Đặt tên package (không được trùng trên PyPI)
    version="0.1.0",  # Phiên bản
    packages=find_packages(),  # Tự động tìm các thư mục con chứa code
    install_requires=[],  # Danh sách dependencies nếu có
    author="Tên của bạn",
    author_email="email@example.com",
    description="Mô tả ngắn về package",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/my_package",  # Liên kết GitHub nếu có
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Yêu cầu phiên bản Python
)
