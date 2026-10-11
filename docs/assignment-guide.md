# Assignment No. 2 — execution and report guide

## Q1: CI/CD, Docker and Docker Compose
1. Create the GitHub repository and upload the kit.
2. Use Codespaces to unpack the archive into the repository root, then commit and push the files.
3. Open Actions and select `DevOps ML Monitor CI/CD`.
4. Capture the successful run showing unit tests, Docker build, Compose configuration, Compose startup and API smoke tests.
5. In a Codespace terminal, run `docker compose up --build -d`, then `docker compose ps`.
6. Capture the running services and API health response at `/health`.

## Q2: MLflow, model versioning, Prometheus and Grafana
1. Start the stack with `docker compose up --build -d`.
2. Open the forwarded MLflow port 5001. Open the experiment named `DevOps ML Monitor`.
3. Open the run `startup-training`; show logged parameters, accuracy metric, and registered model `DevOpsDemoModel`. Model version numbering can increase each time the API restarts.
4. Open API port 5000 and use `/predict` with JSON body `{"features":[5.1,3.5,1.4,0.2]}`.
5. Open Prometheus port 9090 and go to Status → Targets. Confirm `devops-ml-api` is UP.
6. Open Grafana port 3000. Demo credentials are admin/admin unless changed. Open the provisioned dashboard `DevOps ML Monitor`.
7. Send a few predictions so the request counters increase, then refresh the dashboard.

## Q3: End-to-end pipeline
1. Create Jira epic `ML Prediction and Monitoring`.
2. Create stories for prediction API, experiment tracking/model registration, container build, automated tests, Compose deployment, and metrics dashboard.
3. In GitHub, create branch `feature/monitoring-dashboard`, make a meaningful change, commit it, open a pull request, review checks, and merge.
4. Capture the workflow run, Compose services, MLflow run/model version, Prometheus target and Grafana dashboard.
5. Use `architecture.mmd` as the source for the architecture diagram. It can be rendered in a Mermaid-compatible editor or pasted into the report as a Mermaid diagram if supported.

## Suggested Jira story and acceptance criteria
- **Prediction API:** As a user, I want to submit four numeric features and receive a prediction. Acceptance: valid input returns a prediction and class; malformed or missing features return HTTP 400.
- **Experiment tracking:** As a developer, I want training parameters and accuracy logged. Acceptance: a run appears in the `DevOps ML Monitor` experiment with parameters and an accuracy metric.
- **Model registry:** As a developer, I want the trained model registered with a version. Acceptance: `DevOpsDemoModel` appears in MLflow Model Registry with a version.
- **Containerization:** As a developer, I want the app packaged as a Docker image. Acceptance: `docker build` succeeds and the container starts.
- **Compose deployment:** As an operator, I want API, MLflow, Prometheus and Grafana services orchestrated together. Acceptance: services start and API health endpoint returns HTTP 200.
- **Monitoring:** As an operator, I want to observe request metrics. Acceptance: Prometheus target is UP and Grafana dashboard shows metrics.

## Report structure
1. Aim and learning outcomes
2. Tools and architecture
3. Q1 procedure and screenshots
4. Q2 procedure and screenshots
5. Q3 integration workflow and screenshots
6. Problems encountered and fixes
7. Result and conclusion

Only report outcomes you actually observed. GitHub Actions runs on an ephemeral hosted runner; its Compose smoke test does not provide a permanent public service. A Codespace deployment is also temporary unless you keep the environment running. A persistent cloud deployment requires a separately configured host and credentials.
