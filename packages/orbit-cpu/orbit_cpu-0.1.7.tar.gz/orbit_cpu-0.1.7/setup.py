from setuptools import setup, find_packages

setup(
    name= "orbit_cpu",
    version= "0.1.7",
    author= "abiel almonte",
    packages= find_packages(),
    description= "cpu algorithm for target centric clustering for dense embeddings",
    install_requires=[
        "torch",
        "numpy",
        "faiss-cpu",
        "hdbscan"
    ]
)
