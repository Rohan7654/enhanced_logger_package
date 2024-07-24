from setuptools import setup, find_packages

setup(
    name='enhanced-logger',
    version='0.1.3',
    description='An enhanced logging package for Python with additional features and performance metrics.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='ROHAN',
    author_email='rohanroni2019@gmail.com',
    url='https://github.com/Rohan7654/enhanced_logger_package.git',
    packages=find_packages(),
    install_requires=[
        'requests',
        'psutil',
        'pymongo',
        'psycopg2-binary',
    ],
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6',
    include_package_data=True,
)
