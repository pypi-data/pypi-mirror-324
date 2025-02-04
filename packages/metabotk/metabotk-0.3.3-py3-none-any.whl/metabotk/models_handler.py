import numpy as np
import statsmodels.formula.api as smf
import dill
from metabotk.utils import create_directory


class ModelsHandler:
    """
    Class for fitting models to the data and obtaining residuals

    The class takes a data manager as input, and fits a linear model using the
    formula specified in the constructor for each metabolite. The residuals
    are then extracted from the fitted models and returned as a pandas DataFrame.

    If a path to a directory is provided, the fitted models will be saved as
    pickle files in that directory.

    Attributes:
        dataset (DataManager): DataManager instance containing the data
        formula (str): formula used to fit the linear model
        merged (DataFrame): merged dataframe of sample metadata and data
        residuals (DataFrame): dataframe of residuals, initially full of NaNs
    """

    def __init__(self, dataset) -> None:
        """
        Initialize the class.

        Parameters:
            dataset (DataManager): DataManager instance containing the data
            formula (str): formula used to fit the linear model
            models_path (str): path to directory where models will be saved
        """
        self.dataset = dataset
        self.merged = self.dataset.ops.merge_sample_metadata_data()
        self.residuals = self.dataset.data.copy()
        self.residuals.loc[:] = np.nan

    def fit_linear_model(self, metabolite, formula):
        """
        Fit an ordinary least squares (OLS) linear model using the formula specified in the constructor.

        Parameters:
            metabolite (str): name of metabolite to fit model for
            formula (str): list of variables to include in the formula after '~' , in form var1 + var2 + C(var3) where C indicates a categorical variable. !!! DO NOT INCLUDE THE METABOLITE NAME, IT IS AUTOMATICALLY INCLUDED BEFORE THE ~

        Returns:
            residuals (Series): residuals from the fitted model
            model (RegressionResults): fitted model
        """
        model = smf.ols(f"Q('{metabolite}') ~ {formula}", self.merged)
        fitted_model = model.fit()
        residuals = fitted_model.resid
        return residuals, model

    def get_linear_model_residuals(self, formula, models_path=None):
        """
        Fit linear model for each metabolite and extract residuals.

        Parameters:
            formula (str): list of variables to include in the formula after '~' , in form var1 + var2 + C(var3) where C indicates a categorical variable.
            models_path (str): path to directory where models will be saved

        Returns:
            residuals (DataFrame): dataframe of residuals for all metabolites
        """
        if formula == "":
            self.residuals = self.dataset.data.copy()
            return self.residuals
        else:
            if models_path:
                create_directory(models_path)
            for metabolite in self.dataset.metabolites:
                residuals, model = self.fit_linear_model(metabolite, formula)
                self.residuals[metabolite] = residuals
                if models_path:
                    with open(f"{models_path}/{metabolite}.pickle", "wb") as handle:
                        dill.dump(model, handle)
            return self.residuals
