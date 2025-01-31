# Combined Bukmacherska

**Combined Bukmacherska** is a comprehensive project that provides tools for analyzing sports statistics and using machine learning to assist in betting strategies. The package offers utilities for training machine learning models, statistical analysis, and data visualization.

## Features

- **Train Machine Learning Models**: A suite of classifiers, including Random Forest, Gradient Boosting, SVM, and more.
- **Statistical Analysis**: Analyze team performance metrics like average goals scored/conceded.
- **Mathematical Utilities**: Tools for Gamma distribution, Beta distribution, and Poisson probabilities.
- **Visualizations**: Generate line, bar, and 3D plots for data analysis.

## Installation

Clone the repository and install dependencies:

```bash
git clone <repository-url>
cd combined_bukmacherska
pip install -r requirements.txt

Usage Examples
Train Machine Learning Models

from combined_bukmacherska.train_models import train_models, predict_with_models

# Example data
X_train, X_test, y_train, y_test = ...  # Replace with your dataset
models = train_models(X_train, y_train)
predictions = predict_with_models(models, X_test)

from combined_bukmacherska.statistics import analiza_statystyczna, oblicz_statystyki_druzyny

druzyna1 = {'zdobyte': 30, 'stracone': 20}
druzyna2 = {'zdobyte': 25, 'stracone': 15}
mecze = 10

statystyki1, statystyki2 = analiza_statystyczna(druzyna1, druzyna2, mecze)

from combined_bukmacherska.visualizations import rysuj_wykresy

rysuj_wykresy(statystyki1['średnia zdobytych'], statystyki1['średnia straconych'], 
              statystyki2['średnia zdobytych'], statystyki2['średnia straconych'])


git clone https://github.com/your-repository/combined_bukmacherska2.git

from combined_bukmacherska2 import train_models

# Example usage
X_train, y_train = ...  # Your training data
models = train_models(X_train, y_train)

from combined_bukmacherska2 import predict_with_models

# Example usage
X_test = ...  # Your test data
predictions = predict_with_models(models, X_test)

from combined_bukmacherska2 import plot_results

# Example usage
plot_results(predictions, team1_lambda, team2_lambda, team1_avg_conceded, team2_avg_conceded)
