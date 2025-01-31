from setuptools import setup, find_packages


setup(name='flyrl',
      version='0.3.5',
      description='A package of reinforcement learning environments for flight '
                  'control using the JSBSim flight dynamics model.',
      url='https://github.com/ieayvaz/flyrl',
      author='ieayvaz',
      license='MIT',
      install_requires=[
            'numpy',
            'gym',
            'matplotlib',
      ],
      packages=find_packages(),
      classifiers=[
            'License :: OSI Approved :: MIT License',
            'Development Status :: 2 - Pre-Alpha',
            'Intended Audience :: Science/Research',
            'Programming Language :: Python :: 3.6',
            'Topic :: Scientific/Engineering :: Artificial Intelligence',
      ],
      python_requires='>=3.6',
      include_package_data=True,
      zip_safe=False)
