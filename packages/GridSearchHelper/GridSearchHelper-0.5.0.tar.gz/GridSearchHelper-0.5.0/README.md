# GridSearchHelper

A Python library to simplify hyperparameter tuning using scikit-learn's GridSearchCV. Automate parameter grid generation for various machine learning models and optimize your model's performance with ease.

[![PyPI version](https://badge.fury.io/py/gridsearchhelper.svg)](https://badge.fury.io/py/gridsearchhelper)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)

## 🚀 Quick Start

```bash
pip install DridSearchHelper
```

```python
from GridSearchHelper import get_param_grid, perform_grid_search
from sklearn.ensemble import RandomForestRegressor

# Initialize your model
model = RandomForestRegressor()

# Get parameter grid automatically
param_grid = get_param_grid(model)

# Perform grid search
best_params, best_score = perform_grid_search(model, param_grid, X_train, y_train)
```

## 🔑 Key Features

- 🤖 **Automatic Parameter Grid Generation**: No more manual parameter grid definition
- 🔄 **Seamless scikit-learn Integration**: Works directly with GridSearchCV
- 📊 **Multiple Model Support**: Compatible with various scikit-learn models
- 🛠 **Easy to Use**: Simple API with just two main functions

## 📋 Requirements

- Python 3.6+
- scikit-learn
- numpy
- pandas

## 💻 Installation

### From PyPI
```bash
pip install gridsearchhelper
```

### From Source
```bash
git clone https://github.com/alimovabdulla/GridSearchHelper.git
cd GridSearchHelper
pip install .
```

## 📖 Usage Examples

### ElasticNet Example

```python
from GridSearchHelper import get_param_grid, perform_grid_search
from sklearn.linear_model import ElasticNet
from sklearn.preprocessing import StandardScaler

# Prepare your model
model = ElasticNet(alpha=1)

# Scale your features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

# Get parameter grid and perform search
param_grid = get_param_grid(model)
best_params, best_score = perform_grid_search(model, param_grid, X_train_scaled, y_train)
```

### RandomForest Example

```python
from GridSearchHelper import get_param_grid, perform_grid_search
from sklearn.ensemble import RandomForestRegressor

# Initialize model
model = RandomForestRegressor()

# Get grid and optimize
param_grid = get_param_grid(model)
best_params, best_score = perform_grid_search(model, param_grid, X_train, y_train)
```

## 🛠 API Reference

### get_param_grid(model)
Generates parameter grid based on model type.

**Parameters:**
- `model`: scikit-learn model instance

**Returns:**
- Dictionary containing parameter grid

### perform_grid_search(model, param_grid, X_train, y_train)
Performs grid search with cross-validation.

**Parameters:**
- `model`: scikit-learn model instance
- `param_grid`: Parameter grid dictionary
- `X_train`: Training features
- `y_train`: Target values

**Returns:**
- Tuple of (best_parameters, best_score)

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. 🍴 Fork the repository
2. 🌿 Create a feature branch (`git checkout -b feature/amazing-feature`)
3. 💻 Make your changes
4. 📝 Commit your changes (`git commit -m 'Add amazing feature'`)
5. 📤 Push to the branch (`git push origin feature/amazing-feature`)
6. 🔄 Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

Abdullah Alimov - [@alimovabdulla](https://github.com/alimovabdulla)

Project Link: [https://github.com/alimovabdulla/GridSearchHelper](https://github.com/alimovabdulla/GridSearchHelper)

## ⭐️ Show your support

Give a ⭐️ if this project helped you!
