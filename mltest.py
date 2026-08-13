import mlflow

mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("Network Security Test")

with mlflow.start_run():
    mlflow.log_param("test_parameter", "hello")
    mlflow.log_metric("test_accuracy", 0.95)

print("MLflow test successful")