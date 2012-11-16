from distutils.core import setup
import downloads

long_description = open('README.rst').read()

setup(
    name='downloads',
    version=downloads.VERSION,
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
