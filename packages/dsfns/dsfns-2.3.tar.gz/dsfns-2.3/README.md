## Installation

```bash
pip install dsfns
```

# FNS Package

# Version History

    1.1  - Outlier handling - IQR method / Winsorizer / Clip
    1.2  - Missing value imputation - Simple Imputer / Mean, Median, Mode / Numerical data with mean and obj/cat with mode
    1.3  - Outlier Counter, Columns with Outlier and high frequency column finder (single value repeating over 50%)
    1.4  - Data Encoding (label, onehot) and Scaling (MinMax, Standard, Robust)
    1.5  - Fixed general code issues
    1.6  - Redundant Codes removed
    1.7  - Fixed general code issues / issues with return statement
    1.8  - Fixed general code issues / issues with df.sample()
    1.9  - Added Outlier replacement (using Mean, Median or Mode) and Low Variance columns (cols with IQR = 0)
    1.10 - Missing value Interpolation (use with Time series data, Continuous variables with trends etc)
    2.0  - Visualize data with Single and Multiple Line plots
    2.1  - Visualize data with Multiple Regression plots and VIF (Variance Inflation Factor)
    2.2  - Compare model accuracy of multiple models
    2.3  - Added function that outputs various metrics for model evaluation

## FUNCTION DESCRIPTIONS

## OUTLIER HANDLING

1. Replace Outliers using IQR, Upper Limit and Lower Limit:
   Identifies and handles outliers in the specified columns using the Interquartile Range (IQR) method.

    Outlier_IQR(df, columns, whis=1.5)

    - df: DataFrame — The input data in which outliers will be detected.
    - columns: list — List of column names in which outliers need to be identified.
    - whis: float, optional (default=1.5) — The multiplier to define the outlier limits as 1.5 \* IQR by default.

2. Replace outliers with Winsorizer:
   Applies Winsorization to cap outliers in the specified column using either IQR or other capping methods.

    Outlier_Winsorizer(df, column, capping_method='iqr')

    - df: DataFrame — The input data to apply Winsorization.
    - column: str — The name of the column to apply the Winsorization to.
    - capping_method: str, default 'iqr' — Method used to define the outlier thresholds (options: 'iqr' , std, 'quantiles' or 'mad').

3. Clip Outliers using Clip method:
   Clips extreme values to a predefined threshold in the specified columns, effectively handling outliers.

    Outlier_Clip(df, columns)

    - df: DataFrame — The input data to clip outliers from.
    - columns: list — List of columns in which to clip the outliers.

4. Outlier Replacement with Mean, Median or Mode:
   This function is designed to identify and handle outliers in the specified columns of a given DataFrame. It uses the Interquartile Range (IQR) method to determine outliers and replaces the outliers with a user-defined statistic (mean, median, or mode).

    Outlier_MMM(df, columns, type='median')

    - df (DataFrame): The input pandas DataFrame that contains the data to be processed.
      columns (list of str): A list of column names in the DataFrame where outlier handling should be applied.
    - type (optional): It can be one of 'mean', 'median', or 'mode'. The default is 'median'.

5. Outlier Columns:
   Returns a list of columns that contain outliers based on IQR.

    outlierColumns(df):

    - df: DataFrame — The input data to check for outliers.

6. Outlier Counter:
   Counts the number of outliers in the specified columns.

    outlierCount(df, columns)

    - df: DataFrame — The input data to count outliers in.
    - columns: list — List of columns to check for outliers.

## MISSING VALUE IMPUTATION

7. Fill Missing Values with Mean, Median or Mode using df.replace:
   Replaces missing values in the specified columns using a chosen method.

    MissingVal_Repl(df, columns, type='mean')

    - df: DataFrame — The input data in which missing values will be replaced.
    - columns: list — List of column names where missing values need to be replaced.
    - type: str, default 'mean' — The method used for replacement ('mean', 'median', or mode)

8. Fill Missing Values with Mean, Median or Mode with Simple Imputer:
   The MissingVal_Imputer function is designed to handle missing values in specified columns of a pandas DataFrame using different imputation strategies. It replaces missing values (NaN) with appropriate values based on the chosen strategy.

    MissingVal_Imputer(df,columns,strategy='mean')

    - df (pandas.DataFrame): The input DataFrame where missing values need to be imputed.
    - columns (list): A list of column names where missing value imputation is to be applied.
    - strategy (str, default='mean'):The strategy for imputing missing values. Supported values:
      'mean': Replaces missing values with the mean of the column.
      'median': Replaces missing values with the median of the column.
      'mode': Replaces missing values with the most frequent value in the column (converted to 'most_frequent' internally).

9. Fill Missing Values with Mean and/or Mode:
   Identifies and returns all rows in the DataFrame that contain missing values with mean for numeric columns and mode (with index[0]) for object.

    MissingVal_Fillna(df)

    - df: DataFrame — The input data to check for missing values.

10. Interpolate Missing Values:
    This function is designed to handle missing values in a DataFrame by applying interpolation methods to the numerical columns.
    NOTE 1: Interpolation only works for numeric columns.
    NOTE 2: Works better with continuous data

    def MissingVal_Interpolate(df,type='linear')

    - df (DataFrame): The input DataFrame that contains missing (NaN) values.
    - type: Specifies the interpolation method to be used. Options include:
      'linear': Uses linear interpolation (default).
      'polynomial': Uses polynomial interpolation with degree 2 (quadratic).
      'spline': Uses cubic spline interpolation.

## OTHER FUNCTIONS

11. High Frequency Columns:
    Identifies and returns columns where more than the given percentage (default 50%) of values are identical, typically used to detect low-variance or high-frequency columns.

    highFrequency(df, perc=0.5):

    -   df: DataFrame — The input data to identify high-frequency columns.
    -   perc: float, default 0.5 — The percentage threshold for identifying high-frequency columns.

12. Encoder:
    Encodes categorical columns into numeric labels for compatibility with machine learning algorithms.

    Encoding(df, method='label')

    -   df: A Pandas DataFrame containing the dataset.
    -   method: 'label' for label encoding OR 'onehot' for OneHotEncoding

13. Scaler:
    Scales numerical data for better performance during machine learning model training.

    Scaler(df, method='minmax')

    -   df: A Pandas DataFrame containing numeric data.
    -   method: Specifies the scaling technique to use. Options are:
        'minmax' (default): Rescales data to a range of 0 to 1.
        'standard': Standardizes data to have a mean of 0 and a standard deviation of 1.
        'robust': Scales data using the median and interquartile range, making it robust to outliers.

14. Low Variance Columns:
    This function detects columns in a DataFrame with very low variance (i.e., columns where the values are almost constant or do not vary much). Columns with zero variance are identified as low-variance columns. Returns a list of column names that have low variance (IQR = 0)

    LowVarianceCols(df)

    -   df (DataFrame): The input pandas DataFrame for which low variance columns need to be identified.

15. VIF(Variance Inflation Factor)
    The VIF function calculates the Variance Inflation Factor (VIF) for each predictor variable in a dataset, providing insights into multicollinearity. A high VIF (usually greater than 10) indicates that the variable is highly collinear with other predictors and might need to be addressed.

    def VIF(X)

    -   X (DataFrame): A DataFrame containing the independent variables (predictor features) of the dataset.
        NOTE: The dataset should not include the target variable (dependent variable).

## DATA VISUALIZATION

16. LinePlot Multiple:
    Creates a set of subplots where each input column (inpCol) is plotted against the output column (outCol) in individual subplots.

    def Lineplot_Multi(df, inpCol, outCol, figsize=(15, 5))

    -   df (DataFrame): The input dataset containing the columns to plot.
    -   inpCol (list): A list of input columns (features) to plot against the output column.
    -   outCol (str): The output column (target variable) to plot against each input column.
    -   figsize (tuple): Tuple defining the size of the overall figure (default: (15, 5)).

17. LinePlot Single:
    Plots multiple input columns (inpCol) against the output column (outCol) on the same plot, using different lines for each input column, with a legend to identify them.
    NOTE: SCALE THE DATA FOR BETTER VISUALIZATION

    def Lineplot_Single(df, inpCol, outCol)

    -   df (DataFrame): The input dataset containing the columns to plot.
    -   inpCol (list): A list of input columns (features) to plot against the output column.
    -   outCol (str): The output column (target variable) to plot against each input column.

18. RegressionPlot Multiple:
    Creates a set of subplots where each input column (inpCol) is plotted against the output column (outCol) in individual subplots.

    def RegressionPlot_Multiple(df, inpCol, outCol, figsize=(15, 5))

    -   df (DataFrame): The input dataset containing the columns to plot.
    -   inpCol (list): A list of input columns (features) to plot against the output column.
    -   outCol (str): The output column (target variable) to plot against each input column.
    -   figsize (tuple): Tuple defining the size of the overall figure (default: (15, 5)).

## EVALUATION

19. Compare Model Accuracy:
    The CompareAccuracy function is a utility to evaluate and compare the training and testing accuracy of multiple machine learning models on a given dataset. It provides a simple way to benchmark different models and understand their performance.

    def CompareAccuracy(models, x_train, x_test, y_train, y_test):

    -   models (dict): A dictionary where keys are model names (str) and values are their respective model objects.
        Eg:
        models = {
        "svm": SVC(kernel='linear', random_state=42),
        "knn": KNeighborsClassifier(n_neighbors=5)
        }

    -   x_train: The feature set for training the models.
    -   x_test: The feature set for testing the models.
    -   y_train: The target labels for training the models.
    -   y_test: The target labels for testing the models.

20. Metrics_Clf (Classification Metrics):
    The Metrics_Clf function computes the following classification metrics:

    Accuracy: The proportion of correct predictions out of all predictions.
    Precision: The proportion of true positive predictions out of all predicted positives.
    Recall: The proportion of true positive predictions out of all actual positives.
    F1 Score: The harmonic mean of precision and recall, providing a balance between them.
    ROC AUC: The area under the Receiver Operating Characteristic (ROC) curve, indicating the model's ability to distinguish between classes.

    def Metrics_Clf(y_train, y_pred_train, y_test, y_pred_test):

    -   y_train: The true labels of the training set.
    -   y_pred_train: The predicted labels for the training set.
    -   y_test: The true labels of the testing set.
    -   y_pred_test: The predicted labels for the testing set.

21. Metrics_Reg (Regression Metrics):
    The Metrics_Reg function computes the following regression metrics:

    Mean Absolute Error (MAE): The average of the absolute differences between predicted and actual values.
    Mean Squared Error (MSE): The average of the squared differences between predicted and actual values.
    Root Mean Squared Error (RMSE): The square root of the Mean Squared Error, which gives an estimate of the standard deviation of the prediction error.
    R² Score (Coefficient of Determination): A measure of how well the model explains the variance in the data.

    def Metrics_Reg(y_train, y_pred_train, y_test, y_pred_test):

    -   y_train: The true labels of the training set.
    -   y_pred_train: The predicted labels for the training set.
    -   y_test: The true labels of the testing set.
    -   y_pred_test: The predicted labels for the testing set.
