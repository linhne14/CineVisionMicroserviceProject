# Multi-stage build for Movie Service
FROM eclipse-temurin:17-jdk-alpine AS build

# Install Maven
RUN apk add --no-cache maven

WORKDIR /app

# Copy parent pom first 
COPY pom.xml ../pom.xml

# Copy pom.xml for dependency caching
COPY movieService/pom.xml ./

# Download dependencies
RUN mvn dependency:go-offline -B

# Copy source and build
COPY movieService/src ./src
RUN mvn clean package -DskipTests

# Production stage
FROM eclipse-temurin:17-jre-alpine AS production

# Create app user
RUN addgroup --system spring && adduser --system spring --ingroup spring

WORKDIR /app

# Copy jar file
COPY --from=build /app/target/*.jar app.jar

# Change ownership
RUN chown spring:spring /app/app.jar

USER spring

# Labels
LABEL maintainer="cinevision-team"
LABEL version="1.0.0"
LABEL description="CineVision Movie Service"

# Expose port
EXPOSE 8082

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8082/actuator/health || exit 1

# JVM options
ENV JAVA_OPTS="-XX:+UseContainerSupport -XX:MaxRAMPercentage=75.0 -Djava.security.egd=file:/dev/./urandom"

ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar app.jar"]