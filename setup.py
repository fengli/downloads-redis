from distutils.core import setup
VERSION='1.0'

long_description = open('README.md').read()

setup(
    name='downloads',
    version=VERSION,
    packages=['downloads', 
              ],
    description='show top downloads in a certain period of time in redis',
    long_description=long_description,
    author='Feng Li',
    author_email='okidogii@gmail.com',
    license='MIT License',
    url='https://github.com/fengli/downloads-redis.git',
    platforms=["any"],
    classifiers=[
        'Development Status :: 1 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
