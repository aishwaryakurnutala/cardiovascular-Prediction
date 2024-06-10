# Import the required libraries
import numpy as np
import pandas as pd
from scipy.stats import randint 
from collections import Counter

import matplotlib.pyplot as plt 
import seaborn as sns
from statsmodels.formula.api import ols

from plotly.offline import plot, iplot, init_notebook_mode
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.figure_factory as ff

from IPython.display import display_html 

from sklearn.preprocessing import RobustScaler, MinMaxScaler
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
from sklearn.metrics import recall_score, accuracy_score, confusion_matrix, f1_score, matthews_corrcoef
from sklearn.metrics import precision_score, auc, roc_auc_score, roc_curve, precision_recall_curve, classification_report
from scipy.stats import randint 

from collections import Counter


class ReusableUtils():
    
    
    """
    Module of reusable function and utilities that 
    can be reused across notebooks.
    
    """
    
    def __init__(self):
        pass
    
    def setNotebookConfigParams(self):
        
        '''
        Sets the note book 
        configuration parameters.
        
        Params: None
        Return: None
        
        '''
        
        # To display all the columns
        pd.options.display.max_columns = None

        # To display all the rows
        pd.options.display.max_rows = None

        # To map Empty Strings or numpy.inf as Na Values
        pd.options.mode.use_inf_as_na = True

        pd.options.display.expand_frame_repr =  False

        # Set Style
        sns.set(style = "whitegrid")

        # Ignore Warnings
        import warnings
        warnings.filterwarnings('ignore')

        # inline plotting with the Jupyter Notebook
        init_notebook_mode(connected=True)
        
    
    
    def Generate_Model_Test_Classification_Report(self, model, X_test, y_test, model_name=""):

        '''
        Parameters:
            1. y_test - The Ground Truth for each test image.
            2. y_pred - The Predicted label for each image.
            3. model_name - Model Name

        Return Value: 
            NONE.
        '''

        y = 1.05
        # Report Title & Classification Mterics Abbreviations...
        fig, axes = plt.subplots(3, 1, figsize = (8, 3))
        axes[0].text(9, 1.8, "PREDICTION REPORT", fontsize=28, horizontalalignment='center', 
                     color='DarkGreen', weight = 'bold')

        axes[0].axis([0, 10, 0, 10])
        axes[0].axis('off')

        axes[1].text(9, 4, "Model: " + model_name, style='italic', 
                             fontsize=18, horizontalalignment='center', color='DarkRed', weight = 'bold')

        axes[1].axis([0, 10, 0, 10])
        axes[1].axis('off')

        axes[2].text(0, 4, "* 1 - Not Survived\t\t\t\t\t\t\t * 0 - Survived\n".expandtabs(), 
                     style='italic', fontsize=10, horizontalalignment='left', color='orangered')

        axes[2].axis([0, 10, 0, 10])
        axes[2].axis('off')

        scores = []
        metrics = ['F1       ', 'MCC      ', 'Precision', 'Recall   ', 'Accuracy ',
                   'AUC_ROC  ', 'AUC_PR   ']

        # Plot ROC and PR curves using all models and test data...
        y_pred = model.predict(X_test)
        y_pred_probs = model.predict_proba(X_test)[:, 1:]

        fpr, tpr, thresholds = roc_curve(y_test.values.ravel(), y_pred)
        precision, recall, th = precision_recall_curve(y_test.values.ravel(), y_pred_probs)

        # Calculate the individual classification metic scores...
        model_f1_score = f1_score(y_test, y_pred)
        model_matthews_corrcoef_score = matthews_corrcoef(y_test, y_pred)
        model_precision_score = precision_score(y_test, y_pred)
        model_recall_score = recall_score(y_test, y_pred)
        model_accuracy_score = accuracy_score(y_test, y_pred)
        model_auc_roc = auc(fpr, tpr)
        model_auc_pr = auc(recall, precision)

        scores.append([model_f1_score,
                       model_matthews_corrcoef_score,
                       model_precision_score,
                       model_recall_score,
                       model_accuracy_score,
                       model_auc_roc,
                       model_auc_pr])

        sampling_results = pd.DataFrame(columns = ['Classification Metric', 'Score Value'])
        for i in range(len(scores[0])):
            sampling_results.loc[i] = [metrics[i], scores[0][i]]

        sampling_results.index = np.arange(1, len(sampling_results) + 1)

        class_report = classification_report(y_test, y_pred)
        conf_matx = confusion_matrix(y_test, y_pred)

        # Display the Confusion Matrix...
        fig, axes = plt.subplots(1, 3, figsize = (20, 4))
        sns.heatmap(conf_matx, annot=True, annot_kws={"size": 16},fmt='g', cbar=False, cmap="GnBu", ax=axes[0])
        axes[0].set_title("1. Confusion Matrix", fontsize=21, color='darkgreen', weight = 'bold', 
                          style='italic', loc='left', y=y)

        # Classification Metrics
        axes[1].text(5, 1.8, sampling_results.to_string(float_format='{:,.4f}'.format, index=False), style='italic', 
                     fontsize=20, horizontalalignment='center')
        axes[1].axis([0, 10, 0, 10])
        axes[1].axis('off')
        axes[1].set_title("2. Classification Metrics", fontsize=20, color='darkgreen', weight = 'bold', 
                          style='italic', loc='center', y=y)

        # Classification Report
        axes[2].text(0, 1, class_report, style='italic', fontsize=20)
        axes[2].axis([0, 10, 0, 10])
        axes[2].axis('off')
        axes[2].set_title("3. Classification Report", fontsize=20, color='darkgreen', weight = 'bold', 
                          style='italic', loc='center', y=y)

        plt.tight_layout()
        plt.show()

        # AUC-ROC & Precision-Recall Curve
        fig, axes = plt.subplots(1, 2, figsize = (14, 4))

        axes[0].plot(fpr, tpr, label = f"auc_roc = {model_auc_roc:.3f}")
        axes[1].plot(recall, precision, label = f"auc_pr = {model_auc_pr:.3f}")

        axes[0].plot([0, 1], [0, 1], 'k--')
        axes[0].legend(loc = "lower right")
        axes[0].set_xlabel("False Positive Rate")
        axes[0].set_ylabel("True Positive Rate")
        axes[0].set_title("4. AUC - ROC Curve", fontsize=15, color='darkgreen', ha='right', weight = 'bold', 
                          style='italic', loc='center', pad=1, y=y)

        axes[1].legend(loc = "lower left")
        axes[1].set_xlabel("Recall")
        axes[1].set_ylabel("Precision")
        axes[1].set_title("5. Precision - Recall Curve", fontsize=15, color='darkgreen', ha='right', weight = 'bold', 
                          style='italic', loc='center', pad=3, y=y)

        plt.subplots_adjust(top=0.95) 
        plt.tight_layout()
        plt.show()
        
        return None
    
    def plot_model_feature_importances(self, X_train, model):

        '''
        Purpose: 
            Custom function to plot the feature importances of the classifier.
            
            **NOTE: Feature importances specify how much each feature is contributing 
            towards the final prediction value/results. 
            
        Parameters:
            1. model - the model whose feature importances are to be plotted.
            2. X_train - Training dataset.

        Return Value: 
            NONE.
        '''
        
        fig = plt.figure()

        # get the feature importance of the classifier 'model'
        feature_importances = pd.Series(model.feature_importances_,
                                index = X_train.columns) \
                        .sort_values(ascending=False)

        # plot the bar chart
        sns.barplot(x = feature_importances, y = X_train.columns)
        plt.title('Classifier Feature Importance', fontdict = {'fontsize' : 20})
        plt.xticks(rotation = 60)
        plt.show()
        
        return None