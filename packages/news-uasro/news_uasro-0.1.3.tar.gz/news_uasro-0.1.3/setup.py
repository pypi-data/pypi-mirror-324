from setuptools import setup, find_packages

setup(
    name='news_uasro',  # Nama package Anda
    version='0.1.3',  # Versi dari package
    author='Asro',  # Nama Anda atau organisasi
    author_email='asro@raharja.info',  # Email untuk kontak
    description='A utility library to detect media sources.',  # Deskripsi singkat
    long_description=open('README.md').read(),  # Deskripsi panjang dari README
    long_description_content_type='text/markdown',
    url='https://github.com/asroharun6/news_uasro',  # URL ke repositori GitHub
    packages=find_packages(),  # Otomatis menemukan semua paket yang harus diinclude
    include_package_data=True,  # Memastikan file data disertakan
    install_requires=[
        'pandas',  # Contoh, tambahkan semua dependensi yang diperlukan
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',  # Sesuaikan sesuai status pengembangan Anda
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',  # Ganti sesuai lisensi yang Anda pilih
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Versi minimum Python yang dibutuhkan
)
