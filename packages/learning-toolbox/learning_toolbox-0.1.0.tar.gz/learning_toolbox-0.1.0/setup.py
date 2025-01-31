from setuptools import setup, find_packages

setup(
    name='learning_toolbox',  # Choose a name for your library on PyPI
    version='0.1.0',         # Start with a version number
    packages=find_packages(),
    install_requires=[
        'google-generativeai',
        'pdfkit',
        'markdown2',
        'youtube-transcript-api',
    ],
    package_data={
        'learning_toolbox': ['wkhtmltopdf'], # Include wkhtmltopdf binaries if you are distributing them
    },
    include_package_data=True, # Make sure package_data is included in the distribution
    python_requires='>=3.6',  # Specify minimum Python version
    author='Abinash Yadav',       # Your name
    author_email='abinashyadavedu@gmail.com', # Your email
    description='A Python library for generating learning resources using Gemini AI and other tools.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Avinash1286/learning_toolbox', # Project URL
    license='MIT',          # Choose your license
    classifiers=[            # Optional classifiers for PyPI
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)