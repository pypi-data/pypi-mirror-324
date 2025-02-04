from setuptools import setup, find_packages


def parse_requirements(filename):
    with open(filename, mode='r', encoding='utf-8') as file:
        return file.read().splitlines()
    
setup(
    name='ALI-Agent',
    version='0.1.8',
    description='A brief description of your project',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/SophieZheng998/ALI-Agent',
    packages=find_packages(),
    package_data={
           
           '': ['dataset/*', 'dataset/testing/*','dataset/training/*','database/law_traffic/base_test/generated_scenario/*','database/ethic_ETHICS/test/*','database/examiner/*'],  #
       },
    install_requires=parse_requirements('requirements.txt'),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
    entry_points={
        'console_scripts': [
            'ali-agent=aliAgent.cli.main:main',
        ],
    },
)