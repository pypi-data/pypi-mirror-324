from setuptools import setup, find_packages

setup(
    name="mappaforterminal",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "speechrecognition",
        "pyttsx3",
        "requests",
        "torch",
        "transformers",
        "python-dotenv"
    ],
    entry_points={
        "console_scripts": [
            "mappa=mappa:main"
        ]
    },
    author="Your Name",
    description="A voice-controlled terminal assistant",
    url="https://github.com/yourusername/mappa",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
