from setuptools import setup, find_packages

with open("README.md") as readme:
  long_description = readme.read()

setup(
  name='gym-hearts',
  version='0.0.2',
  long_description=long_description,
  url='https://github.com/hisarack/gym-hearts',
  author='Billy Yang',
  author_email='radiohead0401@gmail.com',
  license='MIT',
  description=('OpenAI Gym Hearts Environment for Reinforcement Learning'),
  packages=find_packages(exclude=['test', 'examples']),
  install_requires=['treys', 'gym'],
  platforms='any',
)
