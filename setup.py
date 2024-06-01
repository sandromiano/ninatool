from distutils.core import setup


setup(
      name = 'ninatool',
      version = '0.0.1',
      author = 'Alessandro Miano, Pranav. D. Parakh',
      author_email = 'superconducting.nina@gmail.com',
      description = ('Nonlinear Inductive Network Analyzer tool, a python package'
                      ' to perform analysis of superconducting flux-biased circuits.'),
      license = 'GNU General Public License, version 2',
      packages = ['ninatool', 'ninatool.internal', 'ninatool.internal.mapping_functions', 'ninatool.circuits', 'ninatool.gui'],
      package_data = {'ninatool.internal.mapping_functions' : ['*.txt']},
      include_package_data = True,
      install_requires = []
      )