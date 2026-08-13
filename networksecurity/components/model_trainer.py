import os
import sys

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.artifact_entity import (
    DataTransformationArtifact,
    ModelTrainerArtifact,
)
from networksecurity.entity.config_entity import ModelTrainerConfig

from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.main_utils.utils import (
    save_object,
    load_object,
    load_numpy_array_data,
    evaluate_models,
)
from networksecurity.utils.ml_utils.metric.classification_metric import (
    get_classification_score,
)

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)

import mlflow
import dagshub

dagshub.init(
    repo_owner="Soham007575",
    repo_name="Network_Security_Project",
    mlflow=True,
)


class ModelTrainer:
    def __init__(
        self,
        model_trainer_config: ModelTrainerConfig,
        data_transformation_artifact: DataTransformationArtifact,
    ):
        self.model_trainer_config = model_trainer_config
        self.data_transformation_artifact = data_transformation_artifact

    def track_mlflow(self, best_model, train_metric, test_metric):
        """Log metrics to DagsHub MLflow."""
        try:
            mlflow.set_experiment("Network Security")

            with mlflow.start_run():
                mlflow.log_metric("train_f1", train_metric.f1_score)
                mlflow.log_metric("train_precision", train_metric.precision_score)
                mlflow.log_metric("train_recall", train_metric.recall_score)

                mlflow.log_metric("test_f1", test_metric.f1_score)
                mlflow.log_metric("test_precision", test_metric.precision_score)
                mlflow.log_metric("test_recall", test_metric.recall_score)

                mlflow.sklearn.log_model(best_model, "model")

        except Exception as e:
            print(f"MLflow skipped: {e}")

    def train_model(self, X_train, y_train, x_test, y_test):

        models = {
            "Random Forest": RandomForestClassifier(verbose=1),
            "Decision Tree": DecisionTreeClassifier(),
            "Gradient Boosting": GradientBoostingClassifier(verbose=1),
            "Logistic Regression": LogisticRegression(verbose=1),
            "AdaBoost": AdaBoostClassifier(),
        }

        params = {
            "Decision Tree": {
                "criterion": ["gini", "entropy", "log_loss"]
            },
            "Random Forest": {
                "n_estimators": [8, 16, 32, 128, 256]
            },
            "Gradient Boosting": {
                "learning_rate": [0.1, 0.01, 0.05, 0.001],
                "subsample": [0.6, 0.7, 0.75, 0.85, 0.9],
                "n_estimators": [8, 16, 32, 64, 128, 256],
            },
            "Logistic Regression": {},
            "AdaBoost": {
                "learning_rate": [0.1, 0.01, 0.001],
                "n_estimators": [8, 16, 32, 64, 128, 256],
            },
        }

        print("Evaluating models...")
        model_report = evaluate_models(
            X_train=X_train,
            y_train=y_train,
            X_test=x_test,
            y_test=y_test,
            models=models,
            param=params,
        )

        print("Model evaluation completed")

        best_model_score = max(model_report.values())
        best_model_name = max(model_report, key=model_report.get)
        best_model = models[best_model_name]

        y_train_pred = best_model.predict(X_train)
        train_metric = get_classification_score(y_train, y_train_pred)

        y_test_pred = best_model.predict(x_test)
        test_metric = get_classification_score(y_test, y_test_pred)

        print("Logging to MLflow...")
        self.track_mlflow(best_model, train_metric, test_metric)
        print("MLflow completed")

        preprocessor = load_object(
            self.data_transformation_artifact.transformed_object_file_path
        )

        model_dir_path = os.path.dirname(
            self.model_trainer_config.trained_model_file_path
        )
        os.makedirs(model_dir_path, exist_ok=True)

        network_model = NetworkModel(
            preprocessor=preprocessor,
            model=best_model,
        )

        print("Saving NetworkModel...")
        save_object(
            self.model_trainer_config.trained_model_file_path,
            obj=network_model,
        )

        os.makedirs("final_model", exist_ok=True)
        save_object("final_model/model.pkl", best_model)
        print("Model saved successfully")

        model_trainer_artifact = ModelTrainerArtifact(
            trained_model_file_path=self.model_trainer_config.trained_model_file_path,
            train_metric_artifact=train_metric,
            test_metric_artifact=test_metric,
        )

        logging.info(f"Model trainer artifact: {model_trainer_artifact}")

        return model_trainer_artifact

    def initiate_model_trainer(self):
        try:
            train_arr = load_numpy_array_data(
                self.data_transformation_artifact.transformed_train_file_path
            )
            test_arr = load_numpy_array_data(
                self.data_transformation_artifact.transformed_test_file_path
            )

            x_train = train_arr[:, :-1]
            y_train = train_arr[:, -1]
            x_test = test_arr[:, :-1]
            y_test = test_arr[:, -1]

            return self.train_model(x_train, y_train, x_test, y_test)

        except Exception as e:
            raise NetworkSecurityException(e, sys)