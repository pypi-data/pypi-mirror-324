from setuptools import setup

setup(name='realpass',
      version=0.3,
      description="RealPass is a Python package that generates highly secure, realistic passwords with customizable length and complexity.",
      long_description="RealPass is a Python package that generates strong, realistic passwords by combining uppercase and lowercase letters, numbers, and special characters, with customizable length and complexity settings to ensure both security and practicality. \nContributors:\n\n- Youraj Verma : https://github.com/codex-yv\n- Pooja Velmurugen : https://github.com/Pooja-Velmurugen",
      author="Youraj Verma",
      author_email='yourajverma960@gmail.com',
      packages=['realpass2'],
      install_requires=['numpy', 'python-math', 'random2', 'colorama'],
      url='https://github.com/codex-yv',
      license='codexyv')