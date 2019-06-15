import setuptools

with open("README.md", "r") as f:
   long_description = f.read()

setuptools.setup(
    name="energy_consumption",
    version="0.0.1",
    author="Aditya Vinod Kumar, Rishi Ravikumar",
    author_email="Aditya Vinod Kumar <ads.vinodk@gmail.com>, Rishi Ravikumar <rishiravi.k98@gmail.com>",
    description="Predictive Application for Conserving Energy based on Household Appliances",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/adityavinodk/energy_consumption",
    classifiers=(
        'Programming Language :: Python :: 3.7',
        "License :: MIT License",
        "Operating System :: OS Independent",
    ),
)