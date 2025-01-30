### What is it?
gitlabds is a set of tools designed make it quicker and easier to build predictive models.


### Where to get it?
gitlabds can be installed directly via pip: `pip install gitlabds`.

Alternatively, you can download the source code from Gitlab at https://gitlab.com/gitlab-data/gitlabds and compile locally.


### Main Features	
- **Data prep tools:**
	- Treat outliers
	- Dummy code
	- Miss fill
	- Reduce feature space
	- Split and sample data into train/test
- **Modeling tools:**
	- Easily produce model metrics, feature importance, performance graphs, and lift/gains charts 
    - Generate model insights and prescriptions 

### References and Examples
<details><summary> MAD Outliers </summary>

#### Description
Median Absoutely Deviation for outlier detection and correction. By default will windsor all numeric values in your dataframe that are more than 4 standard deviations above or below the median ('threshold').

`gitlabds.mad_outliers(df, dv=None, min_levels=10, columns = 'all', threshold=4, inplace=False, verbose=True, windsor_threshold=0.01, output_file=None, output_method='a'):`

#### Parameters:
- **_df_** : your pandas dataframe
- **_dv_** : The column name of your outcome. Entering your outcome variable in will prevent it from being windsored. May be left blank there is no outcome variable.
- **_min_levels_** : Only include columns that have at least the number of levels specified. 
- **_columns_** : Will examine at all numeric columns by default. To limit to just  a subset of columns, pass a list of column names. Doing so will ignore any constraints put on by the 'dv' and 'min_levels' paramaters. 
- **_threshold_** : Windsor values greater than this number of standard deviations from the median.
- **_inplace_** : Set to `True` to replace existing dataframe. Set to false to create a new one. Set to `False` to suppress
- **_verbose_** : Set to `True` to print outputs of windsoring being done. Set to `False` to suppress.
- **_windsor_threshold_** : Only windsor values that affect less than this percentage of the population.  
- **_output_file_**: Output syntax to file (e.g. 'my_syntax.py') as a function. Defaults to `None`.
- **_output_method_**: Method of writing file; 'w' to write, 'a' to append. Defaults to 'a'.

#### Returns
- DataFrame with windsored values or None if `inplace=True`.
	
#### Examples:
		
```
#Create a new df; only windsor selected columns; suppress verbose
import gitlabds
new_df = gitlabds.mad_outliers(df = my_df, dv='my_outcome', columns = ['colA', 'colB', 'colC'], verbose=False)
```
```
#Inplace outliers. Will windsor values by altering the current dataframe
import gitlabds
gitlabds.mad_outliers(df = my_df, dv='my_outcome', columns = 'all', inplace=True)
```
</details>
   
<details><summary> Missing Values Check </summary>

#### Description
Check for missing values.

`gitlabds.missing_check(df=None, threshold = 0, by='column_name', ascending=True, return_missing_cols = False):`

#### Parameters:
- **_df_** : your pandas dataframe
- **_threshold_** : The percent of missing values at which a column is considered to have missing values. For example, threshold = .10 will only display columns with more than 10% of its values missing. Defaults to 0.
- **_by_** : Columns to sort by. Defaults to `column_name`. Also accepts `percent_missing`, `total_missing`, or a list.
- **_ascending_** : Sort ascending vs. descending. Defaults to ascending (ascending=True).
- **_return_missing_cols_** : Set to `True` to return a list of column names that meet the threshold criteria for missing. 

#### Returns
- List of columns with missing values filled or None if `return_missing_cols=False`.

#### Examples:
		
```
#Check for missing values using default settings
gitlabds.missing_check(df=my_df, threshold = 0, by='column_name', ascending=True, return_missing_cols = False)
```
```
#Check for columns with more than 5% missing values and return a list of those columns
missing_list = gitlabds.missing_check(df=my_df, threshold = 0.05, by='column_name', ascending=True, return_missing_cols = True) 
```
</details>

<details><summary> Missing Values Fill </summary>

#### Description
Fill missing values using a range of different options.

`gitlabds.missing_fill(df=None, columns='all', method='zero', inplace=False, output_file=None, output_method='a'):`

#### Parameters:
- **_df_** : your pandas dataframe
- **_columns_** : Columns which to miss fill. Defaults to `all` which will miss fill all columns with missing values.
- **_method_** : Options are `zero`, `median`, `mean`, `drop_column`, and `drop_row`. Defaults to `zero`.
- **_inplace_** : Set to `True` to replace existing dataframe. Set to false to create a new one. Set to `False` to suppress
- **_output_file_**: Output syntax to file (e.g. 'my_syntax.py') as a function. Defaults to `None`.
- **_output_method_**: Method of writing file; 'w' to write, 'a' to append. Defaults to 'a'.

#### Returns
- DataFrame with missing values filled or None if `inplace=True`.

#### Examples:
		
```
#Miss fill specificied columns with the mean value into a new dataframe
new_df = gitlabds,missing_fill(df=my_df, columns=['colA', 'colB', 'colC'], method='mean', inplace=False):
```
```
#Miss fill all values with zero in place.
gitlabds.missing_fill(df=my_df, columns='all', method='zero', inplace=True)   
```
</details>

<details><summary> Dummy Code </summary>

#### Description
Dummy code (AKA "one-hot encode") categorical and numeric columns based on the paremeters specificed below. Note: categorical columns will be dropped after they are dummy coded; numeric columns will not

`gitlabds.dummy_code(df, dv=None, columns='all', categorical=True, numeric=True, categorical_max_levels = 20, numeric_max_levels = 10, dummy_na=False, output_file=None, output_method='a'):`

#### Parameters:
- **_df_** : your pandas dataframe
- **_dv_** : The column name of your outcome. Entering your outcome variable in will prevent it from being dummy coded. May be left blank there is no outcome variable.
- **_columns_** : Will examine at all columns by default. To limit to just  a subset of columns, pass a list of column names. 
- **_categorical_** : Set to `True` to attempt to dummy code any categorical column passed via the `columns` parameter.
- **_numeric_** : Set to `True` to attempt to dummy code any numeric column passed via the `columns` parameter.
- **_categorical_max_levels_** : Maximum number of levels a categorical column can have to be eligable for dummy coding.
- **_categorical_max_levels_** : Maximum number of levels a numeric column can have to be eligable for dummy coding.
- **_dummy_na_** : Set to `True` to create a dummy coded column for missing values.
- **_output_file_**: Output syntax to file (e.g. 'my_syntax.py') as a function. Defaults to `None`.
- **_output_method_**: Method of writing file; 'w' to write, 'a' to append. Defaults to 'a'.

#### Returns
- DataFrame with dummy-coded columns. Categorical columns that were dummy coded will be dropped from the dataframe.

#### Examples:
		
```
#Dummy code only categorical columns with a maxinum of 30 levels. Do not dummy code missing values
new_df = gitlabds.dummy_code(df=my_df, dv='my_outcome', columns='all', categorical=True, numeric=False, categorical_max_levels = 30, dummy_na=False)
```
```
#Dummy code only columns specified in the `columns` parameter with a maxinum of 10 levels for categorical and numeric. Also dummy code missing values
new_df = gitlabds.dummy_code(df=my_df, dv='my_outcome', columns= ['colA', colB', 'colC'], categorical=True, numeric=True, categorical_max_levels = 10, numeric_max_levels = 10,  dummy_na=True)
```
</details>

<details><summary> Top Dummies </summary>

#### Description
Dummy codes only categorical levels above a certain threshold of the population. Useful when a column contains many levels but there is not a need or desire to dummy code every level. Currently only works for categorical columns.

`gitlabds.dummy_top(df=None, dv=None, columns = 'all', min_threshold = 0.05, drop_categorial=True, verbose=True, output_file=None, output_method='a'):`

#### Parameters:
- **_df_** : your pandas dataframe
- **_dv_** : The column name of your outcome. Entering your outcome variable in will prevent it from being dummy coded. May be left blank there is no outcome variable.
- **_columns_** : Will examine at all columns by default. To limit to just  a subset of columns, pass a list of column names. 
- **_min_threshold_**: The threshold at which levels will be dummy coded. For example, the default value of `0.05` will dummy code any categorical level that is in at least 5% of all rows.
_ **_drop_categorical_**: Set to `True` to drop categorical columns after they are considered for dummy coding. Set to `False` to keep the original categorical columns in the dataframe.
- **_verbose_** : Set to `True` to print detailed list of all dummy columns being created. Set to `False` to suppress.
- **_output_file_**: Output syntax to file (e.g. 'my_syntax.py') as a function. Defaults to `None`.
- **_output_method_**: Method of writing file; 'w' to write, 'a' to append. Defaults to 'a'.

#### Returns
- DataFrame with dummy coded columns.

#### Examples:
		
```
#Dummy code all categorical levels from all categorical columns whose values are in at least 5% of all rows.
new_df = gitlabds.dummy_top(df=my_df, dv='my_outcome', columns = 'all', min_threshold = 0.05, drop_categorial=True, verbose=True)
```
```
#Dummy code all categorical levels from the selected columns who values are in at least 10% of all rows; suppress verbose printout and retain original categorical columns.
new_df = gitlabds.dummy_top(df=my_df, dv='my_outcome', columns = ['colA', 'colB', 'colC'], min_threshold = 0.10, drop_categorial=False, verbose=False)
```
</details>




<details><summary> Remove Low Variation columns </summary>

#### Description
Remove columns from a dataset that do not meet the variation threshold. That is, columns will be dropped that contain a high percentage of one value.

`gitlabds.remove_low_variation(df=None, dv=None, columns='all', threshold=.98, inplace=False, verbose=True):`

#### Parameters:
- _**df**_ : your pandas dataframe
- **_dv_** : The column name of your outcome. Entering your outcome variable in will prevent it from being removed due to low variation. May be left blank there is no outcome variable.
- **_columns_** : Will examine at all columns by default. To limit to just  a subset of columns, pass a list of column names. 
- **_threshold_**: The maximum percentage one value in a column can represent. columns that exceed this threshold will be dropped. For example, the default value of `0.98` will drop any column where one value is present in more than 98% of rows.
- **_inplace_** : Set to `True` to replace existing dataframe. Set to false to create a new one. Set to `False` to suppress
- **_verbose_** : Set to `True` to print outputs of windsoring being done. Set to `False` to suppress.

#### Returns
- DataFrame with low variation columns dropped or None if `inplace=True`.

#### Examples:
		
```
#Dropped any columns (except for the outcome) where one value is present in more than 95% of rows. A new dataframe will be created.
new_df = gitlabds.remove_low_variation(df=my_df, dv='my_outcome', columns='all', threshold=.95):
```
```
#Dropped any of the selected columns where one value is present in more than 99% of rows. Operation will be done in place on the existing dataframe.
gitlabds.remove_low_variation(df=my_df, dv=None, columns = ['colA', 'colB', 'colC'], threshold=.99, inplace=True):
```
</details>

<details><summary> Correlation Reduction </summary>

#### Description
Reduce the number of columns on a dataframe by dropping columns that are highly correlated with other columns. Note: only one of the two highly correlated columns will be dropped. uses Pearson's correlation coefficient.

`gitlabds.correlation_reduction(df=None, dv=None, threshold = 0.90, inplace=False, verbose=True):`

#### Parameters:
- _**df**_ : your pandas dataframe
- **_dv_** : The column name of your outcome. Entering your outcome variable in will prevent it from being dropped. May be left blank there is no outcome variable.
- **_threshold_**: The threshold above which columns will be dropped. If two variables exceed this threshold, one will be dropped from the dataframe. For example, the default value of `0.90` will identify columns that have correlations greater than 90% to each other and drop one of those columns.
- **_inplace_** : Set to `True` to replace existing dataframe. Set to false to create a new one. Set to `False` to suppress
- **_verbose_** : Set to `True` to print outputs of windsoring being done. Set to `False` to suppress.

#### Returns
- DataFrame with half of highly correlated columns dropped or None if `inplace=True`.

#### Examples:
		
```
#Perform column reduction via correlation using a threshold of 95%, excluding the outcome column. A new dataframe will be created.
new_df = gitlabds.correlation_reduction(df=my_df, dv=None, threshold = 0.95, verbose=True)
```
```
#Perform column reduction via correlation using a threshold of 90%. Operation will be done in place on the existing dataframe.
gitlabds.correlation_reduction(df=None, dv='my_outcome', threshold = 0.90, inplace=True, verbose=True)
```
</details>

<details><summary> Drop Categorical columns </summary>

#### Description
Drop all categorical columns from the dataframe. A useful step before regression modeling, as categorical variables are not used.

`gitlabds.drop_categorical(df, inplace=False):`

#### Parameters:
- _**df**_ : your pandas dataframe
- **_inplace_** : Set to `True` to replace existing dataframe. Set to false to create a new one. Set to `False` to suppress

#### Returns
- DataFrame with categorical columns dropped or None if `inplace=True`.

#### Examples:
		
```
#Dropping categorical columns and creating a new dataframe
new_df = gitlabds.drop_categorical(df=my_df) 
```
```
#Dropping categorical columns in place
gitlabds.drop_categorical(df=my_df, inplace=True) 
```
</details>


<details><summary> Remove Outcome Proxies </summary>

#### Description
Remove columns that are highly correlated with the outcome (target) column.

`gitlabds.dv_proxies(df, dv, threshold=.8, inplace=False):`

#### Parameters:
- _**df**_ : your pandas dataframe
- _**dv**_ : The column name of your outcome.    
- _**threshold**_ : The Pearson's correlation value to the outcome above which columns will be dropped. For example, the default value of `0.80` will identify and drop columns that have correlations greater than 80% to the outcome.    
- **_inplace_** : Set to `True` to replace existing dataframe. Set to false to create a new one. Set to `False` to suppress

#### Returns
- DataFrame with outcome proxy columns dropped or None if `inplace=True`.

#### Examples:
		
```
#Drop columns with correlations to the outcome greater than 70% and create a new dataframe
new_df = gitlabds.dv_proxies(df=my_df, dv='my_outcome', threshold=.7)    
```
```
#Drop columns with correlations to the outcome greater than 80% in place
gitlabds.dv_proxies(df=my_df, dv='my_outcome', threshold=.8, inplace=True)        
```
</details>


<details><summary> Split and Sample Data </summary>

#### Description
This function will split your data into train and test datasets, separating the outcome from the rest of the file. The resultant datasets will be named x_train,y_train, x_test, and y_test.

`gitlabds.split_data(df, train_pct=.7, dv=None, dv_threshold=.0, random_state = 5435):`

#### Parameters:
- _**df**_ : your pandas dataframe
- _**train_pct**_ : The percentage of rows randomdly assigned to the training dataset.
- _**dv**_ : The column name of your outcome.  
- _**dv_threshold**_ : The minimum percentage of rows that much contain a positive instance (i.e. > 0) of the outcome. SMOTE/SMOTE-NC will be used to upsample positive instances until this threshold is reached. Can be disabled by setting to 0. Only accepts values 0 to 0.5
- **random_state** : Random seed to use for splitting dataframe and for up-sampling (if needed)

#### Returns
- 4 dataframes for train and test and a list of model weights.

#### Examples:
		
```
#Split into train and test datasets with 70% of rows in train and 30% in test and change random seed.
x_train, y_train, x_test, y_test, model_weights = gitlabds.split_data(df=my_df, dv='my_outcome', train_pct=0.70, dv_threshold=0, random_state = 64522)
```
```
#Split into train and test datasets with 80% of rows in train and 20% in test; Up-sample if needed to hit 10% threshold.
x_train, y_train, x_test, y_test, model_weights = gitlabds.split_data(df=my_df, dv='my_outcome', train_pct=0.80, dv_threshold=0.1)
```
</details>

<details><summary> Model Metrics </summary>

#### Description
Display a variety of model metrics for linear and logistic predictive models.

`gitlabds.model_metrics(model, x_train, y_train, x_test, y_test, show_graphs=True, f_score = 0.50, classification = True, algo=None, decile_n=10, top_features_n=20):`

#### Parameters:
- _**model**_ : model file from training
- _**x_train**_ : train "predictors" dataframe. 
- _**y_train**_ : train outcome/dv/target dataframe
- _**x_test**_ : test "predictors" dataframe. 
- _**y_test**_ : test outcome/dv/target dataframe
- _**show_graphs**_ : Set to `True` to show visualizations
- _**f_score**_ : Cut point for determining a correct classification. Must also set classification to `True` to enable.
- _**classification**_ : Set to `True` to show classification model metrics (accuracy, precision, recall, F1). Set show_graphs to `True` to display confusion matrix.
- _**algo**_ : Select the algorythm used to display additional model metrics. Supports `rf`, `xgb`, 'logistic', 'elasticnet', and `None`. If your model type is not listed, try `None` and some model metrics should still generate.
- _**top_features_n**_ : Print a list of the top x features present in the model.
- _**decile_n**_ : Specify number of group to create to calculate lift. Defaults to `10` (deciles)



#### Returns
- Separate dataframes for `model metrics` and `lift` and `class_model_metrics` (optional). Lists for `top_features`, and `decile_breaks`.

#### Examples:
		
```
#Display model metrics from an XGBoost model. Return classification metrics using a cut point of 0.30 F-Score
model_metrics, lift, class_metrics, top_features, decile_breaks = gitlabds.model_metrics(model=model, x_train=x_train, y_train=y_train, x_test=x_test, y_test=y_test, show_graphs=True, f_score = 0.3, classification=True, algo='xgb', top_features_n=20, decile_n=10)
```

```
#Display model metrics from a logistic model. Do not return classification metrics and suppress visualizations
model_metrics, lift, top_features, decile_breaks = gitlabds.model_metrics(model=model, x_train=x_train, y_train=y_train, x_test=x_test, y_test=y_test, show_graphs=False, classification=False, algo='logistic',top_features_n=20, decile_n=10)
```
</details>

<details><summary> Marginal Effects </summary>

#### Description
Calculates and returns the marginal effects at the mean (MEM) for predcitor fields.

`gitlabds.marginal_effects(model, x_test, dv_description, field_labels=None):`

#### Parameters:
- _**model**_ : model file from training
- _**x_test**_ : test "predictors" dataframe.
- _**dv_description**_ : Description of the outcome field to be used in text-based insights. 
- _**field_labels**_ : Dict of field descriptions. The key is the field/feature/predictor name. The value is descriptive text of the field. This field is optional and by default will use the field name


#### Returns
- Dataframe of marginal effects.

#### Examples:
		
</details>

<details><summary> Prescriptions </summary>

#### Description
Return "actionable" prescriptions and explanatory insights for each scored record. Insights first list actionable prescriptions follow by explainatory insights. This approach is recommended or linear/logistic methodologies only. Caution should be used if using a black box approach, as manpulating more than one prescription at a time could change a record's model score in unintended ways.  

`gitlabds.prescriptions(model, input_df, scored_df, actionable_fields, dv_description, field_labels=None, returned_insights=5, only_actionable=False, explanation_fields='all'):`

#### Parameters:
- _**model**_ : model file from training
- _**input_df**_ : train "predictors" dataframe. 
- _**scored_df**_ : dataframe containing model scores.
- _**actionable_fields**_ : Dict of actionable fields. The key is the field/feature/predictor name. The value accepts one of 3 values: `Increasing` for prescriptions only when the field increases; `Decreasing` for prescriptions only when the field decreases; `Both` for when the field either increases or decreases.   
- _**dv_description**_ : Description of the outcome field to be used in text-based insights.
- _**field_labels**_ : Dict of field descriptions. The key is the field/feature/predictor name. The value is descriptive text of the field. This field is optional and by default will use the field name
- _**returned_insights**_ : Number of insights per record to return. Defaults to 5
- _**only_actionable**_ : Only return actionable prescriptions
- _**explanation_fields**_ : List of explainable (non-actionable insights) fields to return insights for. Defaults to 'all'

#### Returns
- Dataframe of prescriptive actions. One row per record input.

#### Examples:
		
```
#Return prescriptions for the actionable fields of 'spend', 'returns', and 'emails_sent':
gitlabds.prescriptions(model=model, input_df=my_df, scored_df=my_scores, actionable_fields={'spend':'Increasing', 'returns':'Decreasing', 'emails_sent':'Both'}, dv_description='likelihood to churn', field_labels={'spend':'Dollars spent in last 6 months', 'returns':'Item returns in last 3 months', 'emails_sent':'Marketing emails sent in last month'}, returned_insights=5, only_actionable=True, explaination_fields=['spend', returns'])
```
</details>


## Gitlab Data Science

The [handbook](https://about.gitlab.com/handbook/business-technology/data-team/organization/data-science/) is the single source of truth for all of our documentation. 

### Contributing

We welcome contributions and improvements, please see the [contribution guidelines](CONTRIBUTING.md).

### License

This code is distributed under the MIT license, please see the [LICENSE](LICENSE) file.



