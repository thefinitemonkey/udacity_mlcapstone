# Supress warnings for newer versions of matplotlib
import warnings
warnings.filterwarnings("ignore", category = UserWarning, module = "matplotlib")
# Display inline matplotlib plots with IPython
from IPython import get_ipython
get_ipython().run_line_magic('matplotlib', 'inline')

import matplotlib.pyplot as pl
import numpy as np
import sklearn.learning_curve as curves
from sklearn.tree import DecisionTreeRegressor
from sklearn.cross_validation import ShuffleSplit, train_test_split

def VisualizeModelLearning(X, y):
    # Calculate performance of several models with varying training data sizes
    # then plot the learning and testing scores for each model
    
    # Create 10 cross-validation sets for training and testing
    cv = ShuffleSplit(X.shape[0], n_iter = 10, test_size = .2, random_state = 0)
    print("ShuffleSplit sets: {}".format(cv))
    
    # Generate the training sets of increasing sizes
    train_sizes = np.rint(np.linspace(1, X.shape[0] * .8 - 1, 9)).astype(int)
    print("Visualize training set sizes: {}".format(train_sizes))
    
    # Create the figure window
    fig = pl.figure(figsize = (10, 8))
    
    # Create three different models based on max_depth
    for k, depth in enumerate([1, 3, 4, 5, 6, 10]):
        # Create a decision tree regressor with a max_depth of depth
        regressor = DecisionTreeRegressor(max_depth = depth)
        
        # Calculate training and testing scores
        print("Evaluating depth {}".format(depth))
        sizes, train_scores, test_scores = curves.learning_curve(regressor, X, y, \
               cv = cv, train_sizes = train_sizes, scoring = 'r2')
        
        # Determine the mean and standard deviation for use in smoothing
        train_std = np.std(train_scores, axis = 1)
        train_mean = np.mean(train_scores, axis = 1)
        test_std = np.std(test_scores, axis = 1)
        test_mean = np.mean(test_scores, axis = 1)
        
        # Subplot the learning curve
        ax = fig.add_subplot(3, 2, k + 1)
        ax.plot(sizes, train_mean, 'o-', color = 'r', label = 'Training Score')
        ax.plot(sizes, test_mean, 'o-', color = 'g', label = 'Testing Score')
        ax.fill_between(sizes, train_mean - train_std, train_mean + train_std, alpha = .15, color = 'r')
        ax.fill_between(sizes, test_mean - test_std, test_mean + test_std, alpha = .15, color = 'g')
        print("Results for depth {}: {}".format(depth, test_mean))
        
        # Labels
        ax.set_title('max_depth = %s'%(depth))
        ax.set_xlabel('Number of Training Points')
        ax.set_ylabel('Score')
        ax.set_xlim([0, X.shape[0] * 0.8])
        ax.set_ylim([-.05, 1.05])
        
    # Aesthetics
    ax.legend(loc = 'best')
    fig.suptitle('Decision Tree Regressor Learning Performances', fontsize = 16, y = 1.03)
    fig.tight_layout()
    fig.show()