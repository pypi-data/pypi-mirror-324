from setuptools import setup, find_packages

# Membuka README.md dengan encoding UTF-8
with open('README.md', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='news_uasro',
    version='0.1.4',
    author='Asro',
    author_email='asro@raharja.info',
    description='A utility library to detect media sources.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/asroharun6/news_uasro',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pandas',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
