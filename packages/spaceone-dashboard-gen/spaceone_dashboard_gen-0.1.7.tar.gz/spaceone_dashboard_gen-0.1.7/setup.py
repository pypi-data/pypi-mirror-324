from setuptools import setup, find_packages

setup(
    name='spaceone-dashboard-gen',
    version='0.1.7',
    packages=find_packages(include=['spaceone_dashboard_gen', 'spaceone_dashboard_gen.*']),
    include_package_data=True,
    package_data={
        'spaceone_dashboard_gen': ['templates/*', 'static/*']
    },
    install_requires=[
        'fastapi',
        'uvicorn',
        'pydantic>=2.0',
        'pyyaml',
        'jinja2'
    ],
    author='seolmin',
    author_email='seolmin@megazone.com',
    description='A dashboard generator using FastAPI',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/spaceone-dashboard-gen',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
         'dashboard-gen=uvicorn:main',
    ],
}
)