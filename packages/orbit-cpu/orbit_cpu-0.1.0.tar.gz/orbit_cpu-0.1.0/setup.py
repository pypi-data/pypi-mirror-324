from setuptools import setup, find_packages

setup(
    name= "orbit-cpu",
    packages= find_packages(),
    author= "abiel almonte",
    version= "0.1.0",
    description= "cpu algorithm to cluster dense embeddings",
    install_requires= [
        "numpy",
        "torch",
        "hdbscan",
        "faiss-cpu",
    ]
)
