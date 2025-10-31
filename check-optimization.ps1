# Docker Image Optimization Script
# Kiem tra va optimize Docker images

Write-Host "DOCKER IMAGE OPTIMIZATION REPORT" -ForegroundColor Cyan
Write-Host "=" * 50

# Function to get image size
function Get-ImageSize {
    param($ImageName)
    try {
        $size = docker images --format "table {{.Size}}" $ImageName | Select-Object -Skip 1
        return $size
    }
    catch {
        return "Not found"
    }
}

# Check current images
$images = @("cinevision-frontend", "cinevision-eureka", "cinevision-gateway", "cinevision-user", "cinevision-movie", "cinevision-email")

Write-Host "Current Image Sizes:" -ForegroundColor Yellow
foreach ($image in $images) {
    $size = Get-ImageSize $image
    Write-Host "  $image`: $size" -ForegroundColor Green
}

Write-Host ""
Write-Host "OPTIMIZATION FEATURES IMPLEMENTED:" -ForegroundColor Cyan

Write-Host "Frontend (React + Nginx):" -ForegroundColor Yellow
Write-Host "  + Multi-stage build with alpine base images" -ForegroundColor Green
Write-Host "  + Remove source maps in production" -ForegroundColor Green  
Write-Host "  + Optimized nginx configuration" -ForegroundColor Green
Write-Host "  + Gzip compression with level 6" -ForegroundColor Green
Write-Host "  + Aggressive caching for static assets" -ForegroundColor Green
Write-Host "  + Non-root user execution" -ForegroundColor Green

Write-Host ""
Write-Host "Java Services (Spring Boot):" -ForegroundColor Yellow
Write-Host "  + Multi-stage build with JDK/JRE separation" -ForegroundColor Green
Write-Host "  + JAR layer extraction for better caching" -ForegroundColor Green
Write-Host "  + Optimized JVM flags for containers" -ForegroundColor Green
Write-Host "  + G1GC and String deduplication" -ForegroundColor Green
Write-Host "  + Non-root user execution" -ForegroundColor Green
Write-Host "  + dumb-init for proper signal handling" -ForegroundColor Green

Write-Host ""
Write-Host "Security Optimizations:" -ForegroundColor Yellow
Write-Host "  + Distroless-like approach with minimal packages" -ForegroundColor Green
Write-Host "  + Non-root users for all containers" -ForegroundColor Green
Write-Host "  + Comprehensive .dockerignore files" -ForegroundColor Green
Write-Host "  + Security headers in nginx" -ForegroundColor Green

Write-Host ""
Write-Host "Performance Optimizations:" -ForegroundColor Yellow
Write-Host "  + Layer caching optimization" -ForegroundColor Green
Write-Host "  + Dependency download separation" -ForegroundColor Green
Write-Host "  + Health check improvements" -ForegroundColor Green
Write-Host "  + Resource cleanup after package install" -ForegroundColor Green

Write-Host ""
Write-Host "ESTIMATED SIZE IMPROVEMENTS:" -ForegroundColor Cyan
Write-Host "  Frontend: ~40-60% smaller (removing dev deps, source maps)" -ForegroundColor Green
Write-Host "  Java services: ~20-30% smaller (JRE vs JDK, layer optimization)" -ForegroundColor Green
Write-Host "  Total project: ~35-45% size reduction" -ForegroundColor Green

Write-Host ""
Write-Host "BUILD PERFORMANCE IMPROVEMENTS:" -ForegroundColor Cyan
Write-Host "  + Better Docker layer caching" -ForegroundColor Green
Write-Host "  + Parallel dependency downloads" -ForegroundColor Green  
Write-Host "  + Reduced rebuild times" -ForegroundColor Green
Write-Host "  + Optimized .dockerignore reduces context size" -ForegroundColor Green