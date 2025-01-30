#!/usr/bin/env python
# -*- coding: utf-8 -*--

# Copyright (c) 2022 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

import json
import logging
from typing import Dict, Union

import numpy as np
import pandas as pd

pd.options.mode.chained_assignment = None


# Note to developers: If you make any changes to this class, copy and paste those changes over to
# templates/score_onnx.jinja2 and templates/score_onnx_new.jinja2. We do not yet have an automatic way of doing this.
class ONNXTransformer(object):
    """
    This is a transformer to convert X [pandas.Dataframe, pd.Series] data into Onnx
    readable dtypes and formats. It is Serializable, so it can be reloaded at another time.


    Examples
    --------
    >>> from ads.model.transformer.onnx_transformer import ONNXTransformer
    >>> onnx_data_transformer = ONNXTransformer()
    >>> train_transformed = onnx_data_transformer.fit_transform(train.X, {"column_name1": "impute_value1", "column_name2": "impute_value2"}})
    >>> test_transformed = onnx_data_transformer.transform(test.X)
    """

    def __init__(self):
        self.impute_values = {}
        self.dtypes = None
        self._fitted = False

    @staticmethod
    def _handle_dtypes(X: Union[pd.DataFrame, pd.Series, np.ndarray, list]):
        """Handles the dtypes for pandas dataframe and pandas Series.

        Parameters
        ----------
        X : Union[pd.DataFrame, pd.Series, np.ndarray, list]
            The Dataframe for the training data

        Returns
        -------
        Union[pd.DataFrame, pd.Series, np.ndarray, list]
            The transformed(numerical values are cast to float32) X data
        """
        # Data type cast could be expensive doing it in a for loop
        # Especially with wide datasets
        # So cast the numerical columns first, without loop
        # Then impute missing values
        if isinstance(X, pd.Series):
            series_name = X.name if X.name else 0
            _X = X.to_frame()
            _X = ONNXTransformer._handle_dtypes_dataframe(_X)[series_name]
        elif isinstance(X, pd.DataFrame):
            _X = ONNXTransformer._handle_dtypes_dataframe(X)
        elif isinstance(X, np.ndarray):
            _X = ONNXTransformer._handle_dtypes_np_array(X)
        else:
            # if users convert pandas dataframe with mixed types to numpy array directly
            # it will turn the whole numpy array into object even though some columns are
            # numerical and some are not. In that case, we need to do extra work to identify
            # which columns are really numerical which for now, we only convert to float32
            # if numpy array is all numerical. else, nothing will be done.
            _X = X
        return _X

    @staticmethod
    def _handle_dtypes_dataframe(X: pd.DataFrame):
        """handle the dtypes for pandas dataframe.

        Parameters
        ----------
        X : pandas.DataFrame
            The Dataframe for the training data

        Returns
        -------
        pandas.DataFrame
            The transformed X data
        """
        dict_astype = {}
        for k, v in zip(X.columns, X.dtypes):
            if "int" in str(v) or "float" in str(v) or "bool" in str(v):
                dict_astype[k] = "float32"
        _X = X.astype(dict_astype)
        if len(dict_astype) > 0:
            logging.warning("Numerical values in `X` are cast to float32.")
        return _X

    @staticmethod
    def _handle_dtypes_np_array(X: np.ndarray):
        """handle the dtypes for pandas dataframe.

        Parameters
        ----------
        X : np.ndarray
            The ndarray for the training data

        Returns
        -------
        np.ndarray
            The transformed X data
        """
        if "int" in str(X.dtype) or "float" in str(X.dtype) or "bool" in str(X.dtype):
            _X = X.astype("float32")
            logging.warning("Numerical values in `X` are cast to float32.")
        else:
            _X = X
        return _X

    def fit(
        self,
        X: Union[pd.DataFrame, pd.Series, np.ndarray, list],
        impute_values: Dict = None,
    ):
        """
        Fits the OnnxTransformer on the dataset
        Parameters
        ----------
        X : Union[pandas.DataFrame, pandas.Series, np.ndarray, list]
            The Dataframe for the training data

        Returns
        -------
        Self: ads.Model
            The fitted estimator
        """
        _X = ONNXTransformer._handle_dtypes(X)
        if isinstance(_X, pd.DataFrame):
            self.dtypes = _X.dtypes
        elif isinstance(_X, np.ndarray):
            self.dtypes = _X.dtype
        self.impute_values = impute_values if impute_values else {}
        self._fitted = True
        return self

    def transform(self, X: Union[pd.DataFrame, pd.Series, np.ndarray, list]):
        """
        Transforms the data for the OnnxTransformer.

        Parameters
        ----------
        X: Union[pandas.DataFrame, pandas.Series, np.ndarray, list]
            The Dataframe for the training data

        Returns
        -------
        Union[pandas.DataFrame, pandas.Series, np.ndarray, list]
            The transformed X data
        """
        assert self._fitted, "Call fit_transform first!"
        if self.dtypes is not None and len(self.dtypes) > 0:
            if isinstance(X, list):
                _X = np.array(X).astype(self.dtypes).tolist()
            else:
                _X = X.astype(self.dtypes)
        else:
            _X = X
        _X = ONNXTransformer._handle_missing_value(_X, impute_values=self.impute_values)
        return _X

    @staticmethod
    def _handle_missing_value(
        X: Union[pd.DataFrame, pd.Series, np.ndarray, list], impute_values: Dict
    ):
        """Impute missing values in X according to impute_values.

        Parameters
        ----------
        X: Union[pandas.DataFrame, pandas.Series, np.ndarray, list]
            The Dataframe for the training data

        Raises
        ------
        Exception if X has only one dim, but imputed_values has multiple values.
        NotImplemented if X has the data type that is not supported.

        Returns
        -------
        Union[pandas.DataFrame, pd.Series, np.ndarray, list]
            The transformed X data
        """
        if isinstance(X, np.ndarray):
            X = ONNXTransformer._handle_missing_value_dataframe(
                pd.DataFrame(X), impute_values=impute_values
            ).values
        elif isinstance(X, list):
            X = ONNXTransformer._handle_missing_value_dataframe(
                pd.DataFrame(X), impute_values=impute_values
            ).values.tolist()
        elif isinstance(X, pd.DataFrame):
            X = ONNXTransformer._handle_missing_value_dataframe(
                X, impute_values=impute_values
            )
        elif isinstance(X, pd.Series):
            X = X.replace(r"^\s*$", np.NaN, regex=True)
            if len(impute_values.keys()) == 1:
                for key, val in impute_values.items():
                    X = X.fillna(val)
            else:
                raise Exception(
                    "Multiple imputed values are provided, but `X` has only one dim."
                )
        else:
            raise NotImplemented(
                f"{type(X)} is not supported. Convert `X` to pandas dataframe or numpy array."
            )
        return X

    @staticmethod
    def _handle_missing_value_dataframe(X: pd.DataFrame, impute_values: Dict):
        for idx, val in impute_values.items():
            if isinstance(idx, int):
                X.iloc[:, idx] = (
                    X.iloc[:, idx].replace(r"^\s*$", np.NaN, regex=True).fillna(val)
                )
            else:
                X.loc[:, idx] = (
                    X.loc[:, idx].replace(r"^\s*$", np.NaN, regex=True).fillna(val)
                )
        return X

    def fit_transform(
        self, X: Union[pd.DataFrame, pd.Series], impute_values: Dict = None
    ):
        """
        Fits, then transforms the data
        Parameters
        ----------
        X: Union[pandas.DataFrame, pandas.Series]
            The Dataframe for the training data

        Returns
        -------
        Union[pandas.DataFrame, pandas.Series]
            The transformed X data
        """
        return self.fit(X, impute_values).transform(X)

    def save(self, filename, **kwargs):
        """
        Saves the Onnx model to disk
        Parameters
        ----------
        filename: Str
            The filename location for where the model should be saved

        Returns
        -------
        filename: Str
            The filename where the model was saved
        """
        export_dict = {
            "impute_values": {
                "value": self.impute_values,
                "dtype": str(type(self.impute_values)),
            },
            "dtypes": {}
            if self.dtypes is None
            else {
                "value": {
                    "index": list(self.dtypes.index),
                    "values": [str(val) for val in self.dtypes.values],
                }
                if isinstance(self.dtypes, pd.Series)
                else str(self.dtypes),
                "dtype": str(type(self.dtypes)),
            },
            "_fitted": {"value": self._fitted, "dtype": str(type(self._fitted))},
        }

        with open(filename, "w") as f:
            json.dump(export_dict, f, sort_keys=True, indent=4, separators=(",", ": "))
        return filename

    @staticmethod
    def load(filename, **kwargs):
        """
        Loads the Onnx model to disk
        Parameters
        ----------
        filename: Str
            The filename location for where the model should be loaded

        Returns
        -------
        onnx_transformer: ONNXTransformer
            The loaded model
        """
        # Make sure you have  pandas, numpy, and sklearn imported
        with open(filename, "r") as f:
            export_dict = json.load(f)

        onnx_transformer = ONNXTransformer()
        for key in export_dict.keys():
            if key not in ["impute_values", "dtypes"]:
                try:
                    setattr(onnx_transformer, key, export_dict[key]["value"])
                except Exception as e:
                    print(
                        f"Warning: Failed to reload {key} from {filename} to OnnxTransformer."
                    )
                    raise e
        if "value" in export_dict["dtypes"]:
            if "index" in export_dict["dtypes"]["value"]:
                onnx_transformer.dtypes = pd.Series(
                    data=[
                        np.dtype(val)
                        for val in export_dict["dtypes"]["value"]["values"]
                    ],
                    index=export_dict["dtypes"]["value"]["index"],
                )
            else:
                onnx_transformer.dtypes = export_dict["dtypes"]["value"]
        else:
            onnx_transformer.dtypes = {}
        onnx_transformer.impute_values = export_dict["impute_values"]["value"]
        return onnx_transformer
