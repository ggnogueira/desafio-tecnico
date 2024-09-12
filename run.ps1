$HOME_DIR = Get-Location

if ($args[0] -eq "--restart") {
    Write-Host "Stopping all services"
    docker stop (docker ps -a -q)
}

if ($args[0] -eq "--stop") {
    Write-Host "Stopping all services"
    docker stop (docker ps -a -q)
    exit 0
}

if ($args[0] -eq "--update") {
    Write-Host "update $($args[1]) service"
    Set-Location "$HOME_DIR\docker\$($args[1])"
    docker-compose down
    docker-compose --env-file ../.env.dev up -d --build
    exit 0
}

Write-Host "Starting airflow"
Set-Location "$HOME_DIR\docker\airflow"
docker-compose --env-file ../.env.dev up -d --build

Write-Host "Starting spark"
Set-Location "$HOME_DIR\docker\spark"
docker-compose --env-file ../.env.dev up -d

Write-Host "Starting postgres"
Set-Location "$HOME_DIR\docker\postgres"
docker-compose --env-file ../.env.dev up -d

Write-Host "Starting lambda"
Set-Location "$HOME_DIR\docker\lambda"
docker-compose --env-file ../.env.dev up -d

Write-Host "Starting minio"
Set-Location "$HOME_DIR\docker\minio"
docker-compose --env-file ../.env.dev up -d

Write-Host "Starting metabase"
Set-Location "$HOME_DIR\docker\metabase"
docker-compose --env-file ../.env.dev up -d

Set-Location "$HOME_DIR"
