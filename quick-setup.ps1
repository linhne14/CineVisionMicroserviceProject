#!/usr/bin/env pwsh
# CineVision Microservice Quick Setup Script
# Run this after cloning the repository

Write-Host "🎬 CineVision Microservice - Quick Setup" -ForegroundColor Green
Write-Host "=======================================" -ForegroundColor Green

# Function to check if command exists
function Test-CommandExists {
    param($command)
    try {
        Get-Command $command -ErrorAction Stop | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

# Check prerequisites
Write-Host "`n📋 Checking prerequisites..." -ForegroundColor Yellow

$allGood = $true

# Check Docker
if (Test-CommandExists "docker") {
    $dockerVersion = docker --version
    Write-Host "✅ Docker: $dockerVersion" -ForegroundColor Green
} else {
    Write-Host "❌ Docker not found! Please install Docker Desktop" -ForegroundColor Red
    $allGood = $false
}

# Check Docker Compose
if (Test-CommandExists "docker-compose") {
    $composeVersion = docker-compose --version
    Write-Host "✅ Docker Compose: $composeVersion" -ForegroundColor Green
} else {
    Write-Host "❌ Docker Compose not found!" -ForegroundColor Red
    $allGood = $false
}

# Check Java
if (Test-CommandExists "java") {
    $javaVersion = java --version | Select-Object -First 1
    if ($javaVersion -match "17\.") {
        Write-Host "✅ Java: $javaVersion" -ForegroundColor Green
    } else {
        Write-Host "⚠️ Java 17 required, found: $javaVersion" -ForegroundColor Yellow
        Write-Host "   Please install Java 17 JDK" -ForegroundColor Yellow
    }
} else {
    Write-Host "❌ Java not found! Please install Java 17 JDK" -ForegroundColor Red
    $allGood = $false
}

# Check Maven
if (Test-CommandExists "mvn") {
    $mavenVersion = mvn --version | Select-Object -First 1
    Write-Host "✅ Maven: $mavenVersion" -ForegroundColor Green
} else {
    Write-Host "⚠️ Maven not found, will use wrapper" -ForegroundColor Yellow
}

# Check Node.js
if (Test-CommandExists "node") {
    $nodeVersion = node --version
    Write-Host "✅ Node.js: $nodeVersion" -ForegroundColor Green
} else {
    Write-Host "❌ Node.js not found! Please install Node.js 18+" -ForegroundColor Red
    $allGood = $false
}

# Check npm
if (Test-CommandExists "npm") {
    $npmVersion = npm --version
    Write-Host "✅ npm: $npmVersion" -ForegroundColor Green
} else {
    Write-Host "❌ npm not found!" -ForegroundColor Red
    $allGood = $false
}

if (-not $allGood) {
    Write-Host "`n❌ Please install missing prerequisites first!" -ForegroundColor Red
    Write-Host "See SETUP.md for detailed instructions" -ForegroundColor Yellow
    exit 1
}

Write-Host "`n🔧 Setting up environment..." -ForegroundColor Yellow

# Set JAVA_HOME if not set
if (-not $Env:JAVA_HOME) {
    $possibleJavaPaths = @(
        "C:\Program Files\Java\jdk-17*",
        "C:\Program Files\OpenJDK\jdk-17*",
        "C:\Program Files\Eclipse Adoptium\jdk-17*"
    )
    
    foreach ($path in $possibleJavaPaths) {
        $javaDir = Get-ChildItem $path -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($javaDir) {
            $Env:JAVA_HOME = $javaDir.FullName
            Write-Host "✅ Set JAVA_HOME to: $($Env:JAVA_HOME)" -ForegroundColor Green
            break
        }
    }
    
    if (-not $Env:JAVA_HOME) {
        Write-Host "⚠️ JAVA_HOME not set. Please set it manually:" -ForegroundColor Yellow
        Write-Host '   $Env:JAVA_HOME="C:\Program Files\Java\jdk-17"' -ForegroundColor Yellow
    }
}

# Step 1: Install frontend dependencies
Write-Host "`n📦 Installing frontend dependencies..." -ForegroundColor Yellow
if (Test-Path "frontend/package.json") {
    Push-Location frontend
    try {
        # Remove existing node_modules and package-lock.json if they exist
        if (Test-Path "node_modules") {
            Write-Host "   Removing existing node_modules..." -ForegroundColor Gray
            Remove-Item -Recurse -Force node_modules
        }
        if (Test-Path "package-lock.json") {
            Write-Host "   Removing existing package-lock.json..." -ForegroundColor Gray
            Remove-Item -Force package-lock.json
        }
        
        Write-Host "   Running npm install..." -ForegroundColor Gray
        npm install
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Frontend dependencies installed" -ForegroundColor Green
        } else {
            Write-Host "❌ Frontend npm install failed" -ForegroundColor Red
        }
    }
    finally {
        Pop-Location
    }
} else {
    Write-Host "⚠️ frontend/package.json not found, skipping npm install" -ForegroundColor Yellow
}

# Step 2: Build Java services
Write-Host "`n🏗️ Building Java services..." -ForegroundColor Yellow
if (Test-CommandExists "mvn") {
    Write-Host "   Running mvn clean package..." -ForegroundColor Gray
    mvn clean package -DskipTests
} else {
    Write-Host "   Running ./mvnw clean package..." -ForegroundColor Gray
    if (Test-Path "./mvnw.cmd") {
        ./mvnw.cmd clean package -DskipTests
    } else {
        Write-Host "❌ Maven wrapper not found" -ForegroundColor Red
    }
}

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Java services built successfully" -ForegroundColor Green
} else {
    Write-Host "❌ Java build failed" -ForegroundColor Red
    Write-Host "   Check that JAVA_HOME is set correctly" -ForegroundColor Yellow
}

# Step 3: Start infrastructure
Write-Host "`n🚀 Starting infrastructure..." -ForegroundColor Yellow

Write-Host "   Starting databases and infrastructure..." -ForegroundColor Gray
docker-compose up -d postgres mongodb redis kafka zookeeper zipkin

Write-Host "`n⏰ Waiting 30 seconds for databases to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# Step 4: Build Docker images
Write-Host "`n🐳 Building Docker images..." -ForegroundColor Yellow
Write-Host "   Building Java services..." -ForegroundColor Gray
docker-compose build eureka-server api-gateway movie-service user-service email-service

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Docker images built successfully" -ForegroundColor Green
} else {
    Write-Host "❌ Docker build failed" -ForegroundColor Red
}

# Step 5: Start services
Write-Host "`n🌟 Starting all services..." -ForegroundColor Yellow
docker-compose up -d

Write-Host "`n⏰ Waiting for services to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 20

# Check service health
Write-Host "`n🏥 Checking service health..." -ForegroundColor Yellow
$services = @(
    @{Name="Eureka Server"; URL="http://localhost:8761"},
    @{Name="API Gateway"; URL="http://localhost:8080/actuator/health"},
    @{Name="Movie Service"; URL="http://localhost:8082/actuator/health"},
    @{Name="User Service"; URL="http://localhost:8081/actuator/health"},
    @{Name="Email Service"; URL="http://localhost:8083/actuator/health"},
    @{Name="Frontend"; URL="http://localhost:3000"}
)

foreach ($service in $services) {
    try {
        $response = Invoke-WebRequest -Uri $service.URL -TimeoutSec 5 -ErrorAction SilentlyContinue
        if ($response.StatusCode -eq 200) {
            Write-Host "✅ $($service.Name) is healthy" -ForegroundColor Green
        } else {
            Write-Host "⚠️ $($service.Name) returned status $($response.StatusCode)" -ForegroundColor Yellow
        }
    }
    catch {
        Write-Host "❌ $($service.Name) is not accessible" -ForegroundColor Red
    }
}

Write-Host "`n🎉 Setup complete!" -ForegroundColor Green
Write-Host "=======================================" -ForegroundColor Green
Write-Host "🌐 Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "🚪 API Gateway: http://localhost:8080" -ForegroundColor Cyan
Write-Host "🔍 Eureka Server: http://localhost:8761" -ForegroundColor Cyan
Write-Host "🎬 Movie Service: http://localhost:8082" -ForegroundColor Cyan
Write-Host "👤 User Service: http://localhost:8081" -ForegroundColor Cyan
Write-Host "📧 Email Service: http://localhost:8083" -ForegroundColor Cyan
Write-Host "`n📋 To view logs: docker-compose logs [service-name]" -ForegroundColor Yellow
Write-Host "🔄 To restart: docker-compose restart" -ForegroundColor Yellow
Write-Host "🛑 To stop: docker-compose down" -ForegroundColor Yellow

# Check if any services failed
Write-Host "`n📊 Current service status:" -ForegroundColor Yellow
docker-compose ps