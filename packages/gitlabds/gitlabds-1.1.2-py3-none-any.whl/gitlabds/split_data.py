import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTENC
from sklearn.utils import resample

def split_data(df:pd.DataFrame, train_pct:float=0.7, dv:str=None, dv_threshold:float=0.0, random_state:int=5435):
    """
    This function will split your data into train and test datasets, separating the outcome from the rest of the file. The resultant datasets will be named x_train,y_train, x_test, and y_test.

    Ex: gitlabds.split_data(df, train_pct=.7, dv=None, dv_threshold=.0, random_state = 5435):

    Parameters:


    df : your pandas dataframe

    train_pct : The percentage of rows randomdly assigned to the training dataset.

    dv : The column name of your outcome.

    dv_threshold : The minimum percentage of rows that much contain a positive instance (i.e. > 0) of the outcome. SMOTE/SMOTE-NC will be used to upsample positive instances until this threshold is reached. Can be disabled by setting to 0. Only accepts values 0 to 0.5

    random_state : Random seed to use for splitting dataframe and for up-sampling (if needed)


    Returns

    4 dataframes for train and test and a list of model weights.
    """

    # Determine positive instances of the outcome percentage
    if dv != None:
        # Split Outcome From Other Fields
        x = df.drop(dv, axis=1).copy(deep=True)
        y = df[dv].copy(deep=True)

        # Split Dataset
        x_train, x_test, y_train, y_test = train_test_split(x, 
                                                            y, 
                                                            train_size=train_pct, 
                                                            test_size=np.round(1 - train_pct,3), 
                                                            random_state=random_state, 
                                                            shuffle=True)

        # Get DV Occurance
        dv_pct = len(df[df[dv] != 0]) / len(df)

        # Up-sample if needed
        if dv_pct < dv_threshold:

            print(f'Outcome variable "{dv}" pct: {dv_pct}. Below the dv_threshold value of {dv_threshold}. Will up-sample with SMOTE-NC...')

            # Get numeric columns
            numeric_cols = x_train.select_dtypes(include=["number"]).columns
            
            # Create categorical feature indices list. Should just be dummy features that have 2 values
            cats = [i for i, col in enumerate(numeric_cols) 
                   if x_train[col].nunique(dropna=False) == 2]

            # SMOTENC
            sm = SMOTENC(random_state=random_state,
                         categorical_features=cats,
                         sampling_strategy=dv_threshold / (1 - dv_threshold))
            
            x_train, y_train = sm.fit_resample(x_train, y_train)

            # Assign Model Weights (Non-Instance, Positive Instance)
            model_weights = [1 / ((1 - dv_threshold) / (1 - dv_pct)),
                             1 / (dv_threshold / dv_pct)]

        else:
            model_weights = [1, 1]

    else:
        print("You must enter a DV value")

    return x_train, y_train, x_test, y_test, model_weights
