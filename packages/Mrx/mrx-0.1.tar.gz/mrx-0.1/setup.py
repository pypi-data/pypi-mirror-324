import os
from setuptools import setup, find_packages

setup(
    name="Mrx",
    version="0.1",
    packages=find_packages(),
    install_requires=[],  # ضع المكتبات المطلوبة هنا إن وجدت
    author="Mr X",
    author_email="5a9c41862c@emailawb.pro",
    description="مكتبة Mrx لوظائف متعددة في Python",
    long_description="""🔹 الوظائف المتاحة في المكتبة:
✔ التعامل مع النصوص (تحليل، تحويل، تشفير)  
✔ تشغيل أكواد Python و C++  
✔ التكامل مع Telegram و Telethon  
✔ تحميل الملفات من الإنترنت  
✔ التعامل مع HTML, CSS, JavaScript  
✔ دعم تحليل السورسات والملفات البرمجية  
✔ دعم وظائف متنوعة إضافية  
""",
    long_description_content_type="text/markdown",
    url="https://github.com/MrX/Mrx",  # ضع رابط GitHub أو PyPI الصحيح
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=2.7",  # دعم جميع إصدارات Python الحديثة والقديمة
)
