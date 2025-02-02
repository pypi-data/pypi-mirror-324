from setuptools import setup, find_packages

setup(
    name='ArabSEA',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    package_data={
         'ArabSEA': ['data/*.xlsx'],
        'ArabSEA': ['model.pkl']
        

    },
    install_requires=[
        'botocore==1.27.0', 
        'urllib3==1.26.14',  
        'simpletransformers',
        'pandas',
        'openpyxl',
        'qalsadi',
        'pyarabic',
        'torch',
        'scikit-learn',
    ],
    entry_points={
        'console_scripts': [
            'ArabSEA=ArabSEA.ner_model:ner',
        ],
    },
    author='Salma Nabil, Esraa Magdy, Aya Tarek',
    author_email='s.n.shehab@gmail.com',
    description='A library for extracting Arabic Proper Names',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/ArabSEA',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)
