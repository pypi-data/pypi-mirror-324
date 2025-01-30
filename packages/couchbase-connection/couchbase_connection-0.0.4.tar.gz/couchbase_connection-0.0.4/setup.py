from setuptools import setup, find_packages

VERSION = '0.0.4' 
DESCRIPTION = 'A Couchbase connector for Streamlit'
LONG_DESCRIPTION = 'A Couchbase connector for Streamlit that supports basic CRUD operations and querying. It provides a simple way to interact with a Couchbase database within a Streamlit app.'

# Setting up
setup(
        name="couchbase_connection", 
        version=VERSION,
        author="Viraj Agarwal",
        author_email="virajagarwal15@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        download_url = 'https://github.com/VirajAgarwal1/couchbase_connection/archive/refs/tags/0.0.3.tar.gz',
        install_requires=['couchbase', 'streamlit'],
        keywords=['couchbase', 'streamlit', 'connector', 'couchbase-streamlit-connector', 'python'],
        classifiers= [
            "Development Status :: 4 - Beta",  # Change to 3 - Alpha if it's an early version
            "Intended Audience :: Developers",
            "Topic :: Database",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.13",
            "Operating System :: OS Independent",
        ]
)