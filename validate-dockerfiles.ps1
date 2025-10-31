# CineVision Dockerfiles Validation Script
# Kiem tra tat ca Dockerfiles va .dockerignore files

Write-Host "KIEM TRA APPLICATION DOCKERFILES" -ForegroundColor Cyan
Write-Host "=" * 50

$services = @("frontend", "eureka-server", "api-gateway", "userService", "movieService", "emailService")
$missingFiles = @()
$existingFiles = @()

foreach ($service in $services) {
    $dockerfilePath = ".\$service\Dockerfile"
    $dockerignorePath = ".\$service\.dockerignore"
    
    Write-Host "Checking $service..." -ForegroundColor Yellow
    
    # Check Dockerfile
    if (Test-Path $dockerfilePath) {
        Write-Host "  OK Dockerfile: EXISTS" -ForegroundColor Green
        $existingFiles += "$service/Dockerfile"
    } else {
        Write-Host "  FAIL Dockerfile: MISSING" -ForegroundColor Red
        $missingFiles += "$service/Dockerfile"
    }
    
    # Check .dockerignore
    if (Test-Path $dockerignorePath) {
        Write-Host "  OK .dockerignore: EXISTS" -ForegroundColor Green
        $existingFiles += "$service/.dockerignore"
    } else {
        Write-Host "  FAIL .dockerignore: MISSING" -ForegroundColor Red
        $missingFiles += "$service/.dockerignore"
    }
}

Write-Host ""
Write-Host "SUMMARY:" -ForegroundColor Cyan
Write-Host "Files found: $($existingFiles.Count)" -ForegroundColor Green
Write-Host "Files missing: $($missingFiles.Count)" -ForegroundColor Red

if ($missingFiles.Count -eq 0) {
    Write-Host "ALL APPLICATION DOCKERFILES COMPLETED!" -ForegroundColor Green -BackgroundColor DarkGreen
} else {
    Write-Host "Missing files:" -ForegroundColor Yellow
    $missingFiles | ForEach-Object { Write-Host "   - $_" -ForegroundColor Red }
}

Write-Host ""
Write-Host "DOCKER COMPOSE SERVICES:" -ForegroundColor Cyan
docker-compose config --services