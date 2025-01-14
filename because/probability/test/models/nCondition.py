# ----------------------------------------------------------------------------
# Model Definition
# ----------------------------------------------------------------------------

# Initialize any variables here
t = 0
from random import *


# Describe the test
testDescript = 'N Common Causes Test'

# Define the causal model.
# Each random variable has the following fields:
# - Name
# - List of Parents
# - isObserved (Optional, default True)
# - Data Type (Optional, default 'Numeric')
model =    ['A2', 'A3', 'A4', 'A5', 'A6','B','C', 'D', 'E', 'F', 'I1', 'I2', 'L1', 'L2', 'L3',
			]

# Structural Equation Model for data generation
varEquations = [
                # Bimodal logistic - logistic mixture
                'B = logistic(-2,1) if choice([0,1]) else logistic(3,.75)',
                # Bimodal normal - logistic mixture
                'C = normal(1.5,1) if choice([0,1,1]) else logistic(-.5, 2)',
                # Bimodal logistic - normal mixture
                'D = logistic(1,1) if choice([0,0, 1]) else normal(1.2,.75)',
                # Half-normal distribution
                'E = abs(normal(1,1))',
                # Exponential distribution
                'F = exponential() * .5',
                'f1 = math.tanh(B)',
                'f2 = math.sin(C)',
                'f3 = math.tanh(D-2)',
                'f4 = math.cos(E*1.2)',
                'f5 = math.tanh(F-1)',
                'cn = [f1, f2, f3, f4, f5]',
                'A2 = sum(cn[:1]) + logistic(0,.1)',
                'A3 = sum(cn[:2]) + logistic(0,.1)',
                'A4 = sum(cn[:3]) + logistic(0,.3)',
                'A5 = sum(cn[:4]) + logistic(0,.3)',
                'A6 = sum(cn[:5]) + logistic(0,.3)',
                'I1 = normal(0,1)',
                'I2 = normal(0,1)',
                'L1 = 1.2 * B + logistic(2, max([(B+5)/10, .1]))',
                'L2 =  1.2 * B + f2 + logistic(-2, .5)',
                'L3 = -2 * C  + 2 * B + normal(2, 1.2)',
		        ]
