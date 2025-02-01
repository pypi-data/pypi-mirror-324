from distutils.core import setup

setup(
    name='YOMAPIClient',
    packages=['YOMAPI'],
    version='0.1.21',
    license='MIT',
    description='A PACKAGE TO USE THE SAME YOM API INTERFACE FROM YOM INTEGRATIONS',
    author='Carlos Fuentes',
    author_email='carlos@yom.ai',
    url='https://github.com/YOMCL/yom-pylib-api-client',
    # download_url='https://github.com/user/reponame/archive/v_01.tar.gz',
    keywords=['YOM-INTEGRATIONS'],
    install_requires=[
        'requests',
        'PyJWT',
        'cryptography',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.6',
)
