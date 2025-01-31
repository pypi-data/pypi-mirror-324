from setuptools import setup, find_packages

setup(
    name="streamlit-analytics-cards",
    version="0.0.4",
    description="A custom Streamlit component for analytics cards",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Natalie C",
    url="https://github.com/natxc/streamlit-analytics-cards",
    packages=find_packages(
        include=["streamlit_analytics_cards", "streamlit_analytics_cards.*"]
    ),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.7",
    install_requires=[
        "streamlit >= 0.63",
        "cachetools"
    ],
    extras_require={
        "devel": [
            "wheel",
            "pytest==7.4.0",
            "playwright==1.48.0",
            "requests==2.31.0",
            "pytest-playwright-snapshot==1.0",
            "pytest-rerunfailures==12.0",
        ]
    },
)
