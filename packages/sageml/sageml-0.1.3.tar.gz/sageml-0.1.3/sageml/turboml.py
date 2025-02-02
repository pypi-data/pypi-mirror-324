"""
turboml.py

This module provides the `TurboML` class, our main class for out-of-the-box autoML solution.
It does not provide additional functionalities but it combines other modules to provide a complete solution.
"""
import pandas as pd

from typing import Literal, Optional
import time
import logging

from turbo_ml.preprocessing import sota_preprocessor
from turbo_ml.meta_learning import StatisticalParametersExtractor, ExhaustiveSearch, MetaModelGuesser, HyperTuner
from turbo_ml.algorithms import RandomGuesser as DummyModel
from turbo_ml.base import Model, __ALL_MODELS__
from turbo_ml.utils import options

logging.basicConfig(level=logging.INFO)


class TurboML:
    """
    The `TurboML` class provides an out-of-the-box AutoML solution that automatically
    selects and trains the best machine learning model for a given dataset. It handles
    data validation, statistical parameter extraction, model selection, hyperparameter
    optimization, and model training.

    **Example:**

    ```python
    from turbo_ml import TurboML
    import pandas as pd

    # Load your dataset
    df = pd.read_csv('your_dataset.csv')

    # Initialize TurboML with the dataset and target column
    turboml = TurboML(dataset=df, target='target_column_name')

    # Prepare new data for prediction
    new_data = pd.read_csv('new_data.csv')

    # Make predictions
    predictions = turboml.predict(new_data)
    ```

    **Attributes:**
        model (Model): The machine learning model selected and trained on the dataset.
    """
    logger = logging.getLogger()

    def __init__(self, dataset: pd.DataFrame, target: Optional[str] = None, verbose: bool = True, device: Literal['cpu', 'cuda', 'mps'] = 'cpu', threads: int = 1, hpo_trials: int = 10):
        """
        Initializes the `TurboML` instance by performing the following steps:

        - Validates the input dataset and target column.
        - Extracts statistical parameters from the dataset.
        - Selects the best machine learning model based on dataset characteristics.
        - Optimizes hyperparameters (to be implemented).
        - Trains the selected model on the dataset.

        Args:
            dataset (pd.DataFrame): The input dataset containing features and the target variable.
            target (Optional[str]): The name of the target column in the dataset.

        Raises:
            NotImplementedError: If the target column is not provided.
            Exception: If dataset description, model optimization, or model training fails.

        Notes:
            - The `target` parameter is currently required. Automatic target detection is not yet implemented.
            - Model selection and hyperparameter optimization functionalities are placeholders and should be implemented.
        """
        options.device = device
        options.threads = threads
        self.logger.setLevel(
            'INFO') if verbose else self.logger.setLevel('ERROR')
        self.logger.info("Initializing TurboML...")
        self.model: Model = DummyModel()
        start_time = time.time()
        if target is None:
            # target = find_target() TODO: to be implemented
            raise NotImplementedError(
                "Target automatic detection is not implemented yet, provide target column name")
        self._input_check(dataset, target)
        target_data = dataset[target]
        data = dataset.drop(columns=[target])
        try:
            self.preprocessor = sota_preprocessor()
            data = self.preprocessor.fit_transform(data)
            target_data = self.preprocessor.fit_transform_target(target_data)
        except Exception:
            raise Exception("Preprocessing failed")
        self.logger.info('Preprocessing completed')
        try:
            extractor = StatisticalParametersExtractor(data, target_data)
            dataset_params = extractor.describe_dataset()
        except Exception:
            raise Exception("Dataset description failed")
        self.logger.info(
            'Dataset parameters found, trying to guess best model')
        data_operations = time.time()

        try:
            guesser = MetaModelGuesser()
            self.model = guesser.predict(dataset_params)
        except Exception:
            raise Exception('Model optimization failed')
        model_guessing_time = time.time()

        model_name = self.model.__class__.__name__
        self.logger.info(f'''Model guessed: {
            model_name}, searching for better model (Currently disabled, unless guessing model is DummyModel)''')
        if isinstance(self.model.__class__, DummyModel):
            try:
                search = ExhaustiveSearch()
                self.model = search.predict(data, target_data)
                self.logger.info(f'Looked at {search.counter} models')
            except Exception:
                self.logger.info('Trying to find better model failed')
        model_selection_time = time.time()

        try:
            tuner = HyperTuner()
            hyperparameters = tuner.optimize_hyperparameters(
                self.model.__class__, (data, target_data), dataset_params.task, dataset_params.num_classes, dataset_params.target_features, device, hpo_trials, threads)
            self.model = self.model.__class__(**hyperparameters)
        except Exception:
            self.logger.info('Hyperparameter optimization failed')
        hpo_time = time.time()

        model_name = self.model.__class__.__name__
        self.logger.info(f"Training {model_name} model")
        try:
            self.model.train(data, target_data)
        except Exception:
            raise Exception('Model training failed')
        end_time = time.time()
        self.times = {
            'total': end_time - start_time,
            'data_ops': data_operations - start_time,
            'guessing': model_guessing_time - data_operations,
            'AS': model_selection_time - model_guessing_time,
            'HPO': hpo_time - model_selection_time,
            'training': end_time - hpo_time
        }
        self.logger.info(f"{model_name} model trained successfully")
        self.logger.info(f"Data operations time: {self.times['data_ops']}")
        self.logger.info(f"Model guessing time: {self.times['guessing']}")
        self.logger.info(f"Model selection time: {self.times['AS']}")
        self.logger.info(f"Model HPO time: {self.times['HPO']}")
        self.logger.info(f"Model training time: {self.times['training']}")
        self.logger.info(f"Total time: {self.times['total']}")

    def _input_check(self, dataset: pd.DataFrame, target: str):
        assert dataset is not None and isinstance(dataset, pd.DataFrame)
        assert len(dataset) > 0
        assert target is not None and isinstance(target, str)
        assert target in dataset.columns

    def predict(self, X: pd.DataFrame) -> pd.Series:
        """
        Generates predictions using the trained model.

        Args:
            X (pd.DataFrame): A DataFrame containing the input features for prediction.

        Returns:
            pd.Series: A Series containing the predicted values.
        """
        X = self.preprocessor.transform(X)
        result = self.model.predict(X)
        return result  # TODO: inverse transform target

    def __call__(self, X: pd.DataFrame) -> pd.Series:
        """
        Generates predictions using the trained model. Call method is just wrapper for predict method.

        Args:
            X (pd.DataFrame): A DataFrame containing the input features for prediction.

        Returns:
            pd.Series: A Series containing the predicted values.
        """
        return self.predict(X)
