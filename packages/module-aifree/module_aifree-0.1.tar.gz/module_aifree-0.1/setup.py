from setuptools import setup, find_packages

setup(
    name='module_aifree',
    version='0.1',
    packages=find_packages(),
    package_data={
        'module_aifree': ['*.txt'],  # Включаем все .txt файлы в пакет
    },
    install_requires=[
        'pandas',
        'PyQt5',
        'g4f',
        'black',
        'keyboard',
    ],
    entry_points={
        'console_scripts': [
            'run_neural_network_app=module_aifree.neural_network_app:main',
        ],
    },
    author='maga22maga44',
    author_email='maga22maga44@gmail.com',
    description='A library for running a neural network GUI application.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
