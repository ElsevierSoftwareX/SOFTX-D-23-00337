"""

3. FORM - Structural Reliability
==============================================

The benchmark problem is a simple structural reliability problem
defined in a two-dimensional parameter space consisting of a resistance :math:`R` and a stress :math:`S`. The failure
happens when the stress is higher than the resistance, leading to the following limit-state function:

.. math:: \\textbf{X}=\{R, S\}

.. math:: g(\\textbf{X}) = R - S

The two random variables are independent  and  distributed
according to:

.. math:: R \sim N(200, 20)

.. math:: S \sim N(150, 10)
"""

#%% md
#
# Initially we have to import the necessary modules.

#%%

import matplotlib.pyplot as plt
import numpy as np

from UQpy.distributions import Normal
from UQpy.reliability import FORM
from UQpy.run_model.RunModel import RunModel
from UQpy.run_model.model_execution.PythonModel import PythonModel

model = PythonModel(model_script='local_pfn.py', model_object_name="example1")
RunModelObject = RunModel(model=model)

dist1 = Normal(loc=200., scale=20.)
dist2 = Normal(loc=150., scale=10.)
Q = FORM(distributions=[dist1, dist2], runmodel_object=RunModelObject, tolerance_u=1e-5, tolerance_beta=1e-5)
Q.run()

# print results
print('Design point in standard normal space: %s' % Q.design_point_u)
print('Design point in original space: %s' % Q.design_point_x)
print('Hasofer-Lind reliability index: %s' % Q.beta)
print('FORM probability of failure: %s' % Q.failure_probability)
print(Q.state_function_gradient_record)


# Supporting function
def multivariate_gaussian(pos, mu, sigma):
    n = mu.shape[0]
    sigma_det = np.linalg.det(sigma)
    sigma_inv = np.linalg.inv(sigma)
    N = np.sqrt((2 * np.pi) ** n * sigma_det)
    fac = np.einsum('...k,kl,...l->...', pos - mu, sigma_inv, pos - mu)
    return np.exp(-fac / 2) / N


N = 60
XX = np.linspace(150, 250, N)
YX = np.linspace(120, 180, N)
XX, YX = np.meshgrid(XX, YX)

XU = np.linspace(-3, 3, N)
YU = np.linspace(-3, 3, N)
XU, YU = np.meshgrid(XU, YU)

# Mean vector and covariance matrix in the original space
parameters = [[200, 20], [150, 10]]
mu_X = np.array([parameters[0][0], parameters[1][0]])
Sigma_X = np.array([[parameters[0][1] ** 2, 0.0], [0.0, parameters[1][1] ** 2]])

# Mean vector and covariance matrix in the standard normal space
mu_U = np.array([0., 0.])
Sigma_U = np.array([[1., 0.0], [0.0, 1]])

# Pack X and Y into a single 3-dimensional array for the original space
posX = np.empty(XX.shape + (2,))
posX[:, :, 0] = XX
posX[:, :, 1] = YX
ZX = multivariate_gaussian(posX, mu_X, Sigma_X)

# Pack X and Y into a single 3-dimensional array for the standard normal space
posU = np.empty(XU.shape + (2,))
posU[:, :, 0] = XU
posU[:, :, 1] = YU
ZU = multivariate_gaussian(posU, mu_U, Sigma_U)

# Figure 4a
plt.figure()
plt.rcParams["figure.figsize"] = (12, 12)
plt.rcParams.update({'font.size': 22})
plt.plot(parameters[0][0], parameters[1][0], 'r.')
plt.plot([0, 200], [0, 200], 'k', linewidth=5)
plt.plot(Q.design_point_x[0][0], Q.design_point_x[0][1], 'bo', markersize=12)
plt.contour(XX, YX, ZX, levels=20)
plt.xlabel(r'$X_1$')
plt.ylabel(r'$X_2$')
plt.text(170, 182, '$X_1 - X_2=0$',
         rotation=45,
         horizontalalignment='center',
         verticalalignment='top',
         multialignment='center')
plt.ylim([120, 200])
plt.xlim([130, 240])
plt.grid()
plt.title('Original space')
plt.axes().set_aspect('equal', 'box')
plt.show()

# Figure 4b
plt.figure()
plt.rcParams["figure.figsize"] = (12, 12)
plt.rcParams.update({'font.size': 22})
plt.plot([0, Q.design_point_u[0][0]], [0, Q.design_point_u[0][1]], 'b', linewidth=2)
plt.plot([0, -3], [5, -1], 'k', linewidth=5)
plt.plot(Q.design_point_u[0][0], Q.design_point_u[0][1], 'bo', markersize=12)
plt.contour(XU, YU, ZU, levels=20)
plt.axhline(0, color='black')
plt.axvline(0, color='black')
plt.plot(0, 0, 'r.')

plt.xlabel(r'$U_1$')
plt.ylabel(r'$U_2$')
plt.text(-1.0, 1.1, '$U^\star$=({:1.2f}, {:1.2f})'.format(-2.0, 1.0),
         rotation=0,
         horizontalalignment='center',
         verticalalignment='top',
         multialignment='center')

plt.text(-2.1, 2.05, '$20U_1 - 10U_2 + 50=0$',
         rotation=63,
         horizontalalignment='center',
         verticalalignment='top',
         multialignment='center')

plt.text(-1.5, 0.7, r'$\overrightarrow{\beta}$',
         rotation=0,
         horizontalalignment='center',
         verticalalignment='top',
         multialignment='center')

plt.text(0.02, -0.2, '({:1.1f}, {:1.1f})'.format(0.0, 0.0))
plt.ylim([-1, 3])
plt.xlim([-3.5, 2])
plt.grid()
plt.title('Standard Normal space')
plt.axes().set_aspect('equal', 'box')
plt.show()
