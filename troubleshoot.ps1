#!/usr/bin/env pwsh
# CineVision Microservice - Troubleshooting Script
# Run this when encountering issues

Write-Host "🔧 CineVision Troubleshooting Tool" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green

function Show-Menu {
    Write-Host "`nSelect an option:" -ForegroundColor Yellow
    Write-Host "1. Check system requirements" -ForegroundColor White
    Write-Host "2. Reset and rebuild everything" -ForegroundColor White
    Write-Host "3. Check service logs" -ForegroundColor White
    Write-Host "4. Check ports in use" -ForegroundColor White
    Write-Host "5. Fix Java/Maven issues" -ForegroundColor White
    Write-Host "6. Fix Docker issues" -ForegroundColor White
    Write-Host "7. Fix frontend issues" -ForegroundColor White
    Write-Host "8. Test database connections" -ForegroundColor White
    Write-Host "9. Show service URLs" -ForegroundColor White
    Write-Host "0. Exit" -ForegroundColor White
    
    $choice = Read-Host "`nEnter your choice (0-9)"
    return $choice
}

function Check-SystemRequirements {
    Write-Host "`n📋 System Requirements Check" -ForegroundColor Yellow
    Write-Host "=============================" -ForegroundColor Yellow
    
    # Check Docker
    try {
        $dockerVersion = docker --version 2>$null
        Write-Host "✅ Docker: $dockerVersion" -ForegroundColor Green
        
        $dockerStatus = docker info 2>$null
        if ($?) {
            Write-Host "✅ Docker daemon is running" -ForegroundColor Green
        } else {
            Write-Host "❌ Docker daemon is not running" -ForegroundColor Red
            Write-Host "   Please start Docker Desktop" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "❌ Docker not found" -ForegroundColor Red
    }
    
    # Check Java
    try {
        $javaVersion = java --version 2>$null | Select-Object -First 1
        if ($javaVersion -match "17\.") {
            Write-Host "✅ Java: $javaVersion" -ForegroundColor Green
        } else {
            Write-Host "❌ Java 17 required, found: $javaVersion" -ForegroundColor Red
        }
    } catch {
        Write-Host "❌ Java not found" -ForegroundColor Red
    }
    
    # Check Maven
    try {
        $mavenVersion = mvn --version 2>$null | Select-Object -First 1
        Write-Host "✅ Maven: $mavenVersion" -ForegroundColor Green
    } catch {
        Write-Host "⚠️ Maven not found (will use wrapper)" -ForegroundColor Yellow
    }
    
    # Check Node.js
    try {
        $nodeVersion = node --version 2>$null
        Write-Host "✅ Node.js: $nodeVersion" -ForegroundColor Green
    } catch {
        Write-Host "❌ Node.js not found" -ForegroundColor Red
    }
    
    # Check available memory
    $memory = Get-CimInstance -ClassName Win32_OperatingSystem
    $totalMemoryGB = [math]::Round($memory.TotalVisibleMemorySize / 1MB, 2)
    $freeMemoryGB = [math]::Round($memory.FreePhysicalMemory / 1MB, 2)
    
    if ($totalMemoryGB -ge 8) {
        Write-Host "✅ Memory: $totalMemoryGB GB total, $freeMemoryGB GB free" -ForegroundColor Green
    } else {
        Write-Host "⚠️ Memory: $totalMemoryGB GB total (8GB+ recommended)" -ForegroundColor Yellow
    }
}

function Reset-Everything {
    Write-Host "`n🔄 Resetting entire environment..." -ForegroundColor Yellow
    Write-Host "WARNING: This will remove all containers, images, and volumes!" -ForegroundColor Red
    $confirm = Read-Host "Are you sure? (y/N)"
    
    if ($confirm -eq "y" -or $confirm -eq "Y") {
        Write-Host "Stopping all containers..." -ForegroundColor Gray
        docker-compose down -v
        
        Write-Host "Removing all Docker images..." -ForegroundColor Gray
        docker system prune -a -f
        
        Write-Host "Cleaning frontend..." -ForegroundColor Gray
        if (Test-Path "frontend/node_modules") {
            Remove-Item -Recurse -Force frontend/node_modules
        }
        if (Test-Path "frontend/package-lock.json") {
            Remove-Item -Force frontend/package-lock.json
        }
        
        Write-Host "Cleaning Maven targets..." -ForegroundColor Gray
        Get-ChildItem -Path . -Recurse -Name "target" -Directory | ForEach-Object {
            Remove-Item -Recurse -Force $_
        }
        
        Write-Host "✅ Environment reset complete" -ForegroundColor Green
        Write-Host "Run .\quick-setup.ps1 to rebuild" -ForegroundColor Yellow
    } else {
        Write-Host "Reset cancelled" -ForegroundColor Yellow
    }
}

function Check-ServiceLogs {
    Write-Host "`n📜 Service Logs" -ForegroundColor Yellow
    Write-Host "===============" -ForegroundColor Yellow
    
    $services = @("eureka-server", "api-gateway", "movie-service", "user-service", "email-service", "frontend", "postgres", "mongodb")
    
    foreach ($service in $services) {
        Write-Host "`n--- $service ---" -ForegroundColor Cyan
        docker-compose logs --tail=10 $service 2>$null
        if (-not $?) {
            Write-Host "Service $service not running or not found" -ForegroundColor Gray
        }
    }
}

function Check-Ports {
    Write-Host "`n🔌 Checking ports in use..." -ForegroundColor Yellow
    Write-Host "===========================" -ForegroundColor Yellow
    
    $ports = @(3000, 8080, 8081, 8082, 8083, 8761, 5432, 27017, 6379, 9092, 2181, 9411)
    
    foreach ($port in $ports) {
        $connection = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
        if ($connection) {
            $processName = (Get-Process -Id $connection.OwningProcess -ErrorAction SilentlyContinue).ProcessName
            Write-Host "Port $port : IN USE by $processName (PID: $($connection.OwningProcess))" -ForegroundColor Red
        } else {
            Write-Host "Port $port : FREE" -ForegroundColor Green
        }
    }
}

function Fix-JavaMavenIssues {
    Write-Host "`n☕ Fixing Java/Maven Issues" -ForegroundColor Yellow
    Write-Host "===========================" -ForegroundColor Yellow
    
    # Set JAVA_HOME
    Write-Host "Setting JAVA_HOME..." -ForegroundColor Gray
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
    
    # Clean and rebuild
    Write-Host "Cleaning Maven cache..." -ForegroundColor Gray
    if (Test-Path "$env:USERPROFILE\.m2\repository") {
        Remove-Item -Recurse -Force "$env:USERPROFILE\.m2\repository\com\kaankaplan" -ErrorAction SilentlyContinue
    }
    
    Write-Host "Building with Maven..." -ForegroundColor Gray
    mvn clean package -DskipTests -U
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Java build successful" -ForegroundColor Green
    } else {
        Write-Host "❌ Java build failed" -ForegroundColor Red
        Write-Host "Try running: mvn dependency:resolve" -ForegroundColor Yellow
    }
}

function Fix-DockerIssues {
    Write-Host "`n🐳 Fixing Docker Issues" -ForegroundColor Yellow
    Write-Host "========================" -ForegroundColor Yellow
    
    Write-Host "Restarting Docker containers..." -ForegroundColor Gray
    docker-compose down
    docker-compose up -d --build
    
    Write-Host "Checking Docker disk space..." -ForegroundColor Gray
    docker system df
    
    Write-Host "Pruning unused Docker resources..." -ForegroundColor Gray
    docker system prune -f
    
    Write-Host "✅ Docker cleanup complete" -ForegroundColor Green
}

function Fix-FrontendIssues {
    Write-Host "`n⚛️ Fixing Frontend Issues" -ForegroundColor Yellow
    Write-Host "=========================" -ForegroundColor Yellow
    
    Push-Location frontend
    try {
        Write-Host "Removing node_modules and package-lock.json..." -ForegroundColor Gray
        Remove-Item -Recurse -Force node_modules -ErrorAction SilentlyContinue
        Remove-Item -Force package-lock.json -ErrorAction SilentlyContinue
        
        Write-Host "Clearing npm cache..." -ForegroundColor Gray
        npm cache clean --force
        
        Write-Host "Installing dependencies..." -ForegroundColor Gray
        npm install
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Frontend dependencies installed" -ForegroundColor Green
        } else {
            Write-Host "❌ npm install failed" -ForegroundColor Red
            Write-Host "Try running: npm install --legacy-peer-deps" -ForegroundColor Yellow
        }
    }
    finally {
        Pop-Location
    }
}

function Test-DatabaseConnections {
    Write-Host "`n🗄️ Testing Database Connections" -ForegroundColor Yellow
    Write-Host "===============================" -ForegroundColor Yellow
    
    # Test PostgreSQL
    Write-Host "Testing PostgreSQL..." -ForegroundColor Gray
    try {
        $pgTest = docker exec cinevisionmicroserviceproject-postgres-1 psql -U postgres -d cinevision -c "SELECT COUNT(*) FROM movies;" 2>$null
        if ($?) {
            Write-Host "✅ PostgreSQL connection successful" -ForegroundColor Green
            Write-Host "$pgTest" -ForegroundColor Gray
        } else {
            Write-Host "❌ PostgreSQL connection failed" -ForegroundColor Red
        }
    } catch {
        Write-Host "❌ PostgreSQL container not running" -ForegroundColor Red
    }
    
    # Test MongoDB
    Write-Host "Testing MongoDB..." -ForegroundColor Gray
    try {
        $mongoTest = docker exec cinevisionmicroserviceproject-mongodb-1 mongosh --eval "db.adminCommand('ping')" 2>$null
        if ($?) {
            Write-Host "✅ MongoDB connection successful" -ForegroundColor Green
        } else {
            Write-Host "❌ MongoDB connection failed" -ForegroundColor Red
        }
    } catch {
        Write-Host "❌ MongoDB container not running" -ForegroundColor Red
    }
    
    # Test Redis
    Write-Host "Testing Redis..." -ForegroundColor Gray
    try {
        $redisTest = docker exec cinevisionmicroserviceproject-redis-1 redis-cli ping 2>$null
        if ($redisTest -eq "PONG") {
            Write-Host "✅ Redis connection successful" -ForegroundColor Green
        } else {
            Write-Host "❌ Redis connection failed" -ForegroundColor Red
        }
    } catch {
        Write-Host "❌ Redis container not running" -ForegroundColor Red
    }
}

function Show-ServiceUrls {
    Write-Host "`n🌐 Service URLs" -ForegroundColor Yellow
    Write-Host "===============" -ForegroundColor Yellow
    
    $urls = @(
        @{Name="Frontend"; URL="http://localhost:3000"; Description="Main application"},
        @{Name="API Gateway"; URL="http://localhost:8080"; Description="API entry point"},
        @{Name="Eureka Server"; URL="http://localhost:8761"; Description="Service discovery"},
        @{Name="Movie Service"; URL="http://localhost:8082/actuator/health"; Description="Movie management"},
        @{Name="User Service"; URL="http://localhost:8081/actuator/health"; Description="User authentication"},
        @{Name="Email Service"; URL="http://localhost:8083/actuator/health"; Description="Email notifications"},
        @{Name="Zipkin"; URL="http://localhost:9411"; Description="Distributed tracing"}
    )
    
    foreach ($url in $urls) {
        Write-Host "$($url.Name):" -ForegroundColor Cyan -NoNewline
        Write-Host " $($url.URL)" -ForegroundColor White
        Write-Host "  └─ $($url.Description)" -ForegroundColor Gray
    }
}

# Main loop
do {
    $choice = Show-Menu
    
    switch ($choice) {
        "1" { Check-SystemRequirements }
        "2" { Reset-Everything }
        "3" { Check-ServiceLogs }
        "4" { Check-Ports }
        "5" { Fix-JavaMavenIssues }
        "6" { Fix-DockerIssues }
        "7" { Fix-FrontendIssues }
        "8" { Test-DatabaseConnections }
        "9" { Show-ServiceUrls }
        "0" { 
            Write-Host "`nGoodbye! 👋" -ForegroundColor Green
            break 
        }
        default { 
            Write-Host "`nInvalid choice. Please try again." -ForegroundColor Red 
        }
    }
    
    if ($choice -ne "0") {
        Write-Host "`nPress any key to continue..." -ForegroundColor Gray
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    }
} while ($choice -ne "0")