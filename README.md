# ninatool

The 'Nonlinear Inductive Network Analyzer' (NINA) tool is a python package to analyze superconducting circuits, based on the theory presented in the paper 

*Hamiltonian extrema of an arbitrary Josephson circuit*, available at https://arxiv.org/abs/2302.03155.

The main functionality of NINA is to compute the Tayolor expansion coefficient of the effective potential energy function of an arbitrary 
flux-biased superconducting loop. The loop can host any combination of Josephson junctions (JJs) and linear inductances.

NINA includes a simple GUI to allow the user to quickly test the properties of a desired superconducting structure (branches and single loops are currently supported, more general structures will be available in the future).

# units

NINA uses dimensionless units for currents, inductances and energies.

Typically, the user would first fix the desired current units $I_\mathrm{U}$, then the inductance units $L_\mathrm{U}$ and energy units $E_\mathrm{U}$ can be derived from current_units as:

$L_\mathrm{U} = \dfrac{\Phi_0}{2\pi I_\mathrm{U}}$ 

$E_\mathrm{U} = \dfrac{\Phi_0 I_\mathrm{U}}{2\pi}$ 

where $\Phi_0 \approx 2.067 \times 10^{-15}$ Wb is the magnetic flux quantum.

# installation instructions

To install NINA, execute "pip install ." in the package directory.

If you install NINA in a conda environment, be sure to have PyQt5-dependent installations already installed via conda, or the "pip install ." might break some functionalities. This will be fixed in the future with a dedicated conda installer.

It is important to not install NINA as a .egg (DON'T execute "python setup.py install"), as it will fail to load some necessary .txt files.

# citing NINA

If you use NINA for your research, be a good citizen and cite this article https://arxiv.org/abs/2302.03155.
