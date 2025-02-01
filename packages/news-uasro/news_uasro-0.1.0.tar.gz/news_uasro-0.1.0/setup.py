from setuptools import setup, find_packages

setup(
    name='news_uasro',
    version='0.1.0',
    author='Asro',
    author_email='asro@raharja.info',
    description='Library untuk mengidentifikasi sumber berita di Indonesia.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/asroharun6/news_uasro',
    packages=find_packages(),
    include_package_data=True,  # Pastikan data non-Python seperti CSV termasuk
    install_requires=[
        'pandas',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
