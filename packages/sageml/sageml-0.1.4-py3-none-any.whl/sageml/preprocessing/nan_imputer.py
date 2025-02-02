import pandas as pd
import numpy as np
from ..base.preprocess import Preprocessor
from sklearn.impute import SimpleImputer


class NanImputer(Preprocessor):
    numerical_imputer = SimpleImputer(strategy="mean")
    numerical_target_imputer = SimpleImputer(strategy="mean")
    categorical_imputer = SimpleImputer(strategy="most_frequent")
    categorical_target_imputer = SimpleImputer(strategy="most_frequent")

    def fit_transform(
        self, data: pd.DataFrame, nan_threshold: float = 1.0
    ) -> pd.DataFrame:
        nans = data.isna().sum() / len(data)
        self.cols_to_drop = nans[nans > nan_threshold]
        data.drop(columns=self.cols_to_drop.index, inplace=True)
        og_cols = data.columns
        data = data.apply(lambda x: x.astype(
            object) if x.isin([0, 1]).all() and not pd.api.types.is_float_dtype(x) else x)
        numerical_cols = data.select_dtypes(include=[np.number])
        categorical_cols = data.select_dtypes(
            include=[object, "category", "string", np.bool_]
        ).map(lambda x: x if pd.isna(x) else str(x))
        if not numerical_cols.empty:
            numerical_cols = pd.DataFrame(
                self.numerical_imputer.fit_transform(numerical_cols),
                columns=numerical_cols.columns,
            )
        if not categorical_cols.empty:
            categorical_cols = pd.DataFrame(
                self.categorical_imputer.fit_transform(categorical_cols),
                columns=categorical_cols.columns,
            )
        data = pd.concat([numerical_cols if not numerical_cols.empty else None,
                         categorical_cols if not categorical_cols.empty else None], axis=1)
        data = data.apply(lambda x: x.astype(
            bool) if x.isin([0, 1]).all() and not pd.api.types.is_float_dtype(x) else x)
        return data[og_cols]

    def fit_transform_target(self, target: pd.Series) -> pd.Series:
        if target.isin([0, 1]).all() and not pd.api.types.is_float_dtype(target):
            target = target.astype(object)
        if pd.api.types.is_float_dtype(target):
            target = pd.Series(
                self.numerical_target_imputer.fit_transform(
                    np.transpose([target]))[:, 0]
            )
        else:
            target = pd.Series(
                self.categorical_target_imputer.fit_transform(
                    np.transpose([target]))[:, 0]
            )
        if target.isin([0, 1]).all() and not pd.api.types.is_float_dtype(target):
            target = target.astype(bool)
        return target

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        data.drop(columns=self.cols_to_drop.index, inplace=True)
        og_cols = data.columns
        data = data.apply(lambda x: x.astype(
            object) if x.isin([0, 1]).all() and not pd.api.types.is_float_dtype(x) else x)
        numerical_cols = data.select_dtypes(include=[np.number])
        categorical_cols = data.select_dtypes(
            include=[object, "category", "string", np.bool_]
        ).map(lambda x: x if x is np.nan else str(x))
        if not numerical_cols.empty:
            numerical_cols = pd.DataFrame(
                self.numerical_imputer.fit_transform(numerical_cols),
                columns=numerical_cols.columns,
            )
        if not categorical_cols.empty:
            categorical_cols = pd.DataFrame(
                self.categorical_imputer.fit_transform(categorical_cols),
                columns=categorical_cols.columns,
            )

        data = pd.concat([numerical_cols if not numerical_cols.empty else None,
                          categorical_cols if not categorical_cols.empty else None], axis=1)
        data = data.apply(lambda x: x.astype(
            bool) if x.isin([0, 1]).all() and not pd.api.types.is_float_dtype(x) else x)
        return data[og_cols]

    def transform_target(self, target: pd.Series) -> pd.Series:
        if target.isin([0, 1]).all() and not pd.api.types.is_float_dtype(target):
            target = target.astype(object)
        if pd.api.types.is_float_dtype(target):
            target = pd.Series(
                self.numerical_target_imputer.transform(
                    np.transpose([target]))[:, 0]
            )
        else:
            target = pd.Series(
                self.categorical_target_imputer.transform(
                    np.transpose([target]))[:, 0]
            )
        if target.isin([0, 1]).all() and not pd.api.types.is_float_dtype(target):
            target = target.astype(bool)
        return target


def main():

    dataset = pd.DataFrame(
        {
            "A": [1, np.nan, 3, 4],
            "B": [10, np.nan, 30, np.nan],
            "C": ["a", "b", np.nan, "d"],
            "D": [0, np.nan, np.nan, 0],
            "E": [1, np.nan, "c", 0],
            "target": [45, np.nan, 69, np.nan],
        }
    )
    data = dataset.drop(columns=["target"])
    target = dataset["target"]
    print("Before NanHandling:")
    print(data)
    print(target)
    print()
    nan_imputer = NanImputer()
    data = nan_imputer.fit_transform(data)
    print("After data NanHandling:")
    print(data)
    print()
    data = pd.DataFrame(
        {
            "A": [np.nan, 2.5, np.nan, 4.5],
            "B": [11, 21, np.nan, 41],
            "C": [np.nan, "b", "c", np.nan],
            "D": [np.nan, 1, np.nan, 1],
            "E": [1, 0.2, "c", np.nan],
        }
    )
    data = nan_imputer.transform(data)
    print("NanHandling more data:")
    print(data)
    print()
    target = nan_imputer.fit_transform_target(target)
    print("After target NanHandling:")
    print(target)


if __name__ == "__main__":
    main()
