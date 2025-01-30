from setuptools import setup, find_packages

setup(
    name='shabakhti',
    version='0.8',
    packages=find_packages(),
    install_requires=[
        'tensorflow',
        'numpy',
        'pillow',
        'opencv-python'
    ],
    entry_points={
        'console_scripts': [
            'shabakhti=shabakhti:shabakhti',
        ],
    },
    author='mohammad_shabakhti',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
