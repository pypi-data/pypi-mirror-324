# Copyright 2025 Sergio Nava Muñoz and Mario Graff Guerrero

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np
from sklearn.base import clone
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import pandas as pd
from CompStats.tests.test_performance import DATA


def test_Perf():
    """Test perf"""
    from CompStats.interface import Perf

    X, y = load_iris(return_X_y=True)
    _ = train_test_split(X, y, test_size=0.3)
    X_train, X_val, y_train, y_val = _
    m = LinearSVC().fit(X_train, y_train)
    hy = m.predict(X_val)
    ens = RandomForestClassifier().fit(X_train, y_train)
    perf = Perf(y_val, hy, forest=ens.predict(X_val), num_samples=50)
    assert 'alg-1' in perf.predictions
    assert 'forest' in perf.predictions
    assert str(perf) is not None


def test_Perf_statistic():
    """Test statistic"""
    from CompStats.interface import Perf

    X, y = load_iris(return_X_y=True)
    _ = train_test_split(X, y, test_size=0.3)
    X_train, X_val, y_train, y_val = _
    ens = RandomForestClassifier().fit(X_train, y_train)
    perf = Perf(y_val, forest=ens.predict(X_val), num_samples=50)
    assert 'forest' in perf.statistic()


def test_Perf_plot():
    """Test plot"""

    from CompStats.interface import Perf

    X, y = load_iris(return_X_y=True)
    _ = train_test_split(X, y, test_size=0.3)
    X_train, X_val, y_train, y_val = _
    ens = RandomForestClassifier().fit(X_train, y_train)
    perf = Perf(y_val, forest=ens.predict(X_val), num_samples=50)
    perf.plot()


def test_Perf_clone():
    """Test Perf.clone"""
    from CompStats.interface import Perf

    X, y = load_iris(return_X_y=True)
    _ = train_test_split(X, y, test_size=0.3)
    X_train, X_val, y_train, y_val = _
    ens = RandomForestClassifier().fit(X_train, y_train)
    perf = Perf(y_val, forest=ens.predict(X_val), num_samples=50)
    samples = perf.statistic_samples._samples
    perf2 = clone(perf)
    perf2.error_func = lambda y, hy: (y != hy).mean()
    assert 'forest' in perf2.statistic_samples.calls
    assert np.all(samples == perf2.statistic_samples._samples)


def test_Perf_best():
    """Test Perf.best"""
    from CompStats.interface import Perf

    X, y = load_iris(return_X_y=True)
    _ = train_test_split(X, y, test_size=0.3)
    X_train, X_val, y_train, y_val = _
    m = LinearSVC().fit(X_train, y_train)
    hy = m.predict(X_val)
    ens = RandomForestClassifier().fit(X_train, y_train)
    perf = Perf(y_val, hy, forest=ens.predict(X_val), num_samples=50)
    assert len(perf.best) == 2


def test_Perf_difference():
    """Test difference"""
    from CompStats.interface import Perf, Difference

    X, y = load_iris(return_X_y=True)
    _ = train_test_split(X, y, test_size=0.3)
    X_train, X_val, y_train, y_val = _
    m = LinearSVC().fit(X_train, y_train)
    hy = m.predict(X_val)
    ens = RandomForestClassifier().fit(X_train, y_train)
    perf = Perf(y_val, hy, forest=ens.predict(X_val), num_samples=50)
    diff = perf.difference()
    assert isinstance(diff, Difference)
    assert isinstance(str(diff), str)


def test_Difference_plot():
    """Test difference plot"""
    from CompStats.interface import Perf

    X, y = load_iris(return_X_y=True)
    _ = train_test_split(X, y, test_size=0.3)
    X_train, X_val, y_train, y_val = _
    m = LinearSVC().fit(X_train, y_train)
    hy = m.predict(X_val)
    ens = RandomForestClassifier().fit(X_train, y_train)
    perf = Perf(y_val, hy, forest=ens.predict(X_val), num_samples=50)
    diff = perf.difference()
    diff.plot()


def test_Perf_dataframe():
    """Test Perf with dataframe"""
    from CompStats.interface import Perf

    df = pd.read_csv(DATA)
    perf = Perf(df, num_samples=50)
    assert 'INGEOTEC' in perf.statistic()


def test_Perf_call():
    """Test Perf call"""
    from CompStats.interface import Perf

    X, y = load_iris(return_X_y=True)
    _ = train_test_split(X, y, test_size=0.3)
    X_train, X_val, y_train, y_val = _
    m = LinearSVC().fit(X_train, y_train)
    hy = m.predict(X_val)
    ens = RandomForestClassifier().fit(X_train, y_train)
    hy2 = ens.predict(X_val)
    perf = Perf(y_val, num_samples=50)
    for xx in [hy, hy2]:
        _ = perf(xx)
        print(_)
    perf(hy, name='alg-2')
    assert 'alg-2' not in perf._statistic_samples.calls
    assert 'alg-1' in perf._statistic_samples.calls