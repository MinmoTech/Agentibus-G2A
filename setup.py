from setuptools import setup, find_packages

setup(name='agentibus',
      version='0.1',
      description='Monitor game deal sites!',
      url='https://github.com/juligreen/GameDeals',
      author='Julius Dehner',
      author_email='julius.dehner@gmail.com',
      packages=find_packages(),
      package_data={'': ["resources/*"]},
      include_package_data=True,
      install_requires=[
          'selenium',
          'pytest',
          'python-telegram-bot',
          'schedule',
      ],
      entry_points={
          'console_scripts':
              ['agentibus = agentibus.Main:execute']
      }),
