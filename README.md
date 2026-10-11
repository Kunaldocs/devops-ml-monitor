# DevOps ML Monitor — Assignment No. 2

A browser-first university lab demo integrating GitHub Actions, Docker Compose, MLflow, Prometheus, and Grafana.

## Services
- Prediction API: Flask + scikit-learn, with `/predict`, `/health`, and `/metrics`
- MLflow: experiment tracking and registered model
- Prometheus: scrapes API metrics
- Grafana: pre-provisioned dashboard
- Docker Compose: runs the full stack

This is a demonstration, not a production system. It uses a synthetic dataset and makes no real-world decisions.

## Repository name
Recommended: `devops-ml-monitor`

## Files
- `app/`: API, model training and tests
- `docker-compose.yml`: local/container orchestration
- `Dockerfile`: container image
- `monitoring/prometheus.yml`: scrape configuration
- `monitoring/grafana/`: provisioned datasource and dashboard
- `.github/workflows/ci-cd.yml`: build, test, container build, Compose smoke test

## Browser-only workflow
1. Create a GitHub repository named `devops-ml-monitor`.
2. Upload this ZIP file to the repository root.
3. Open Codespaces (Code → Codespaces → Create codespace on main) if your account allows it.
4. In its terminal, run:
   ```bash
   unzip -o devops-assignment-2-kit.zip
   cp -R devops-assignment-2-kit/. .
   rm -rf devops-assignment-2-kit
   rm -f devops-assignment-2-kit.zip
   git add -A
   git commit -m "feat: add ML monitoring DevOps stack"
   git push origin main
   ```
   If the ZIP is named differently, adjust the filename in the commands.
5. In GitHub, open Actions and inspect the `DevOps ML Monitor CI/CD` run.
6. For an interactive Docker Compose demonstration, use a Codespace terminal:
   ```bash
   docker compose up --build -d
   docker compose ps
   docker compose logs --tail=80
   ```
7. Open the forwarded ports in Codespaces:
   - API: 5000
   - MLflow: 5001
   - Prometheus: 9090
   - Grafana: 3000 (demo login: admin / admin; change it for any real use)
8. To stop the stack:
   ```bash
   docker compose down
   ```
   To remove stored demo data too:
   ```bash
   docker compose down -v
   ```

Codespaces availability, Docker support, and free usage depend on your GitHub account/organization. If Docker is unavailable there, the GitHub Actions workflow still provides remote automated test/build and Compose smoke-test evidence. Check its logs.

## CI/CD workflow
On pushes to `main` and pull requests to `main`, GitHub Actions installs Python dependencies, runs unit tests, builds the Docker image, validates Compose configuration, starts the stack, waits for the API, tests health and metrics endpoints, then stops the stack. The hosted runner is temporary: its Compose deployment is an integration/smoke-test deployment, not a persistent public service. Run Compose in a Codespace to interact with dashboards during the lab demonstration.

## Endpoints
- `GET /health`: health check
- `GET /metrics`: Prometheus metrics
- `POST /predict` with JSON `{"features":[5.1,3.5,1.4,0.2]}`: sample prediction

## MLflow
At startup the API trains a small model on a synthetic Iris-like dataset, logs parameters and accuracy to MLflow, registers a model version, and saves a local copy into a shared Docker volume for the API to serve. The training is deliberately small so the demo starts quickly. The MLflow UI is available on port 5001.

## Prometheus and Grafana
Prometheus scrapes `api:5000/metrics`. Grafana has a pre-provisioned Prometheus datasource and a dashboard with request count, prediction count, and process uptime. Make predictions to populate the counters.

## Assignment evidence
- Q1: Actions run with tests/build/container/Compose smoke test; `docker compose ps`; app health endpoint.
- Q2: MLflow experiment run with parameters and metric; registered model version; successful `/predict`; Prometheus targets; Grafana dashboard.
- Q3: Jira backlog, repository commits/branches/pull request, workflow run, Compose deployment, architecture diagram, monitoring screenshots.

## Important notes
- Do not put credentials or secrets in the repository.
- The demo Grafana credentials are for lab use only.
- Do not claim that a persistent public deployment exists unless you actually deploy to and verify a persistent host.
- Use an actual teammate for collaboration evidence if required by the instructor.
