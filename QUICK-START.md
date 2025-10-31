# 🎬 CineVision - Hướng Dẫn Clone & Chạy Nhanh

## 🚀 Cách chạy sau khi clone

### 1. Clone repository
```bash
git clone https://github.com/linhne14/CineVisionMicroserviceProject.git
cd CineVisionMicroserviceProject
```

### 2. Chạy setup tự động (KHUYÊN DÙNG)
```powershell
# Windows PowerShell
.\quick-setup.ps1
```

### 3. Hoặc chạy thủ công:

#### Bước 1: Cài frontend dependencies
```bash
cd frontend
npm install
cd ..
```

#### Bước 2: Build Java services  
```bash
# Đảm bảo có Java 17
java --version

# Build tất cả services
mvn clean package -DskipTests
```

#### Bước 3: Khởi động containers
```bash
# Start databases trước
docker-compose up -d postgres mongodb redis kafka zookeeper zipkin

# Chờ 30 giây để DB khởi động xong

# Start services
docker-compose up -d eureka-server api-gateway movie-service user-service email-service frontend
```

## 🌐 Truy cập ứng dụng

| Dịch vụ | URL | Mô tả |
|---------|-----|-------|
| **Ứng dụng chính** | http://localhost:3000 | Frontend React |
| **API Gateway** | http://localhost:8080 | REST API endpoint |  
| **Eureka Dashboard** | http://localhost:8761 | Service registry |
| **Zipkin Tracing** | http://localhost:9411 | Request tracing |

## ⚠️ Lỗi thường gặp

### "Command not found" 
```bash
# Cài thiếu Docker Desktop, Java 17, Maven, Node.js
# Xem SETUP.md để cài đặt chi tiết
```

### "Port already in use"
```bash
# Stop containers hiện tại
docker-compose down

# Kill process đang dùng port
netstat -ano | findstr :8080
taskkill /PID <PID_NUMBER> /F
```

### "Java version issue"
```bash
# Phải dùng Java 17, không phải 8 hoặc 11
java --version

# Set JAVA_HOME nếu cần
$Env:JAVA_HOME="C:\Program Files\Java\jdk-17"
```

### "npm install fails"
```bash
cd frontend
rm -rf node_modules package-lock.json  
npm cache clean --force
npm install
```

### "Database connection failed"
```bash
# Restart databases
docker-compose restart postgres mongodb

# Check logs
docker-compose logs postgres
docker-compose logs mongodb
```

## 🔧 Reset toàn bộ (nếu mọi thứ hỏng)

```bash
# Stop tất cả
docker-compose down -v

# Xóa images
docker system prune -a

# Chạy lại setup
.\quick-setup.ps1
```

## 🛠️ Debug tool

```bash
# Chạy troubleshooting script
.\troubleshoot.ps1

# Sẽ có menu để:
# 1. Check system requirements
# 2. Reset everything  
# 3. Check service logs
# 4. Check ports
# 5. Fix Java/Maven
# 6. Fix Docker
# 7. Fix frontend
# 8. Test databases
```

## 📋 Kiểm tra mọi thứ hoạt động

```bash
# Check containers running
docker-compose ps

# Check service health
curl http://localhost:8080/actuator/health
curl http://localhost:8082/actuator/health  
curl http://localhost:8081/actuator/health
curl http://localhost:8083/actuator/health

# Check database có data
docker exec cinevisionmicroserviceproject-postgres-1 psql -U postgres -d cinevision -c "SELECT COUNT(*) FROM movies;"
# Kết quả phải là: count = 8
```

## 💡 Tips

1. **Chạy từng bước**: Đừng skip bước nào, chạy từ database → services → frontend
2. **Check logs**: Khi có lỗi, luôn check `docker-compose logs [service-name]`  
3. **Resource**: Đảm bảo máy có ít nhất 8GB RAM cho Docker
4. **Network**: Tắt VPN nếu có lỗi Docker network

## 🆘 Nếu vẫn không được

1. Chạy `.\troubleshoot.ps1`  
2. Copy error message và system info
3. Tạo issue trên GitHub với logs đầy đủ

## ✅ Success indicators

Khi setup thành công, bạn sẽ thấy:
- ✅ Frontend tải được tại http://localhost:3000
- ✅ Có 8 movies hiển thị trên trang chủ
- ✅ Đăng ký/đăng nhập hoạt động
- ✅ Database có dữ liệu thật (không phải mock)

**Happy coding! 🎉**