from setuptools import setup

setup(
    name="fsbuddy",
    version="0.1.0",
    entry_points={
        "console_scripts": [
            "fsbuddy=main:main",
        ]
    },
    python_requires=">=3.8",
    install_requires=[
        "send2trash>=1.8.0"  # Ensure the minimum version is specified
    ],
)
