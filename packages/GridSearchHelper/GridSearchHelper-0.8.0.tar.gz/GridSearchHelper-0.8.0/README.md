# 📊 GridSearchHelper: Advanced Hyperparameter Tuning Library

Welcome to **GridSearchHelper**, a powerful and flexible hyperparameter tuning library designed to make model optimization effortless! 🚀

## ✨ Features

- 🔄 **Automated Hyperparameter Grid Generation** for supported models
- 📈 **Seamless Integration** with Scikit-Learn's GridSearchCV
- ⚡ **Supports Classification & Regression Models**
- 🛠️ **Customizable Parameter Grids**
- 🎯 **Easy-to-Use API**

---

## 📌 Installation

```bash
pip install GridSearchHelper
```

---

## 🚀 Quick Start

### Import and Initialize

```python
from GridSearchHelper import perform_grid_search
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_diabetes

# Load dataset
data = load_diabetes()
X, y = data.data, data.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Run Hyperparameter Tuning
best_params, best_score, grid_search = perform_grid_search(
    model_name='Ridge',
    X_train=X_train_scaled,
    y_train=y_train,
    cv_folds=5,
    scoring='neg_mean_squared_error'
)

print(f'Best Parameters: {best_params}')
```

---

## ⚙️ Supported Models

- RandomForestClassifier 🌲
- GradientBoostingClassifier 🔥
- SVC 🛡️
- LogisticRegression 📊
- Ridge 📏
- Many more...

---

## 🔧 Configuration

To add custom hyperparameters, simply pass them as a dictionary:

```python
custom_params = {
    'alpha': [0.01, 0.1, 1, 10],
    'solver': ['auto', 'svd', 'cholesky']
}
perform_grid_search('Ridge', X_train_scaled, y_train, additional_params=custom_params)
```

---

## 📜 License

MIT License © 2025 Abdulla Alimov

---

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

🌟 **Star this repo if you find it useful!**

