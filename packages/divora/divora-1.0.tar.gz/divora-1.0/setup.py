from setuptools import setup

long_description = """
A simple way to train and own your AI models.
"""


setup(
    name="divora",
    packages=["divora"],  # this must be the same as the name above
    version="1.0",
    description="A simple way to train and own your AI models.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Shiloh Pendergraff",
    author_email="shilohpendergraff@gmail.com",
    url="https://divoratech.com",
    keywords=["deep learning", "tensorflow", "text generation"],
    classifiers=[],
    license="Divora/MIT",
    entry_points={
        "console_scripts": ["gpt_2_simple=gpt_2_simple.gpt_2:cmd"],
    },
    python_requires=">=3.6",
    include_package_data=True,
    install_requires=[
        "tensorflow>=2.5.1",
        "regex",
        "requests",
        "tqdm",
        "numpy",
        "toposort",
    ],
)
