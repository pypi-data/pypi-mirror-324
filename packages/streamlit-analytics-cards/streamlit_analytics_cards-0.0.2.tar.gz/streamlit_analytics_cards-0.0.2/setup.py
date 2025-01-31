from setuptools import setup, find_packages

setup(
    name="streamlit-analytics-cards",
    version="0.0.2",
    description="A custom Streamlit component for analytics cards",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Natalie C",
    url="https://github.com/natxc/streamlit-analytics-cards",
    packages=find_packages(
        include=["streamlit_analytics_cards", "streamlit_analytics_cards.*"]
    ),
    include_package_data=True,
    package_data={
        "streamlit_analytics_cards": [
            "frontend/build/*",
            "frontend/build/static/css/*",
            "frontend/build/static/js/*",
            "frontend/build/static/media/*",
            "frontend/build/asset-manifest.json",
            "frontend/build/index.html",
        ]
    },
    install_requires=["streamlit", "cachetools"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
