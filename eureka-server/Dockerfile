# Multi-stage build for Spring Boot application
FROM eclipse-temurin:17-jdk-alpine AS build

# Install Maven and remove cache
RUN apk add --no-cache maven && \
    rm -rf /var/cache/apk/*

# Set working directory
WORKDIR /app

# Copy parent pom first 
COPY pom.xml ../pom.xml

# Copy module pom.xml for dependency caching
COPY eureka-server/pom.xml ./

# Download dependencies (better layer caching)
RUN mvn dependency:go-offline -B && \
    mvn dependency:resolve-sources && \
    rm -rf ~/.m2/repository/org/apache/maven

# Copy source code
COPY eureka-server/src ./src

# Build the application with optimizations
RUN mvn clean package -DskipTests -Dmaven.compile.fork=true && \
    # Extract JAR layers for better caching
    java -Djarmode=layertools -jar target/*.jar extract

# Production stage - distroless for minimal attack surface
FROM eclipse-temurin:17-jre-alpine AS production

# Install curl for health checks and dumb-init, remove cache
RUN apk add --no-cache curl dumb-init && \
    rm -rf /var/cache/apk/*

# Create app user for security
RUN addgroup --system --gid 1001 spring && \
    adduser --system --uid 1001 --ingroup spring spring

# Set working directory
WORKDIR /app

# Copy JAR layers for better caching (if layertools was used)
COPY --from=build --chown=spring:spring /app/dependencies/ ./
COPY --from=build --chown=spring:spring /app/spring-boot-loader/ ./
COPY --from=build --chown=spring:spring /app/snapshot-dependencies/ ./
COPY --from=build --chown=spring:spring /app/application/ ./

# Fallback: copy jar if layertools failed
COPY --from=build --chown=spring:spring /app/target/*.jar app.jar

# Switch to spring user
USER spring

# Add comprehensive labels
LABEL maintainer="cinevision-team" \
      version="1.0.0" \
      description="CineVision Eureka Server" \
      org.opencontainers.image.source="https://github.com/linhne14/CineVisionMicroserviceProject" \
      org.opencontainers.image.vendor="CineVision Team" \
      org.opencontainers.image.title="Eureka Discovery Server"

# Expose port
EXPOSE 8761

# Health check with retry logic
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=5 \
  CMD curl -f http://localhost:8761/actuator/health || exit 1

# Optimized JVM options for containers
ENV JAVA_OPTS="-XX:+UseContainerSupport \
               -XX:MaxRAMPercentage=75.0 \
               -XX:+UseG1GC \
               -XX:+UseStringDeduplication \
               -XX:+OptimizeStringConcat \
               -Djava.security.egd=file:/dev/./urandom \
               -Dspring.backgroundpreinitializer.ignore=true"

# Use dumb-init for proper signal handling
ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD ["sh", "-c", "java $JAVA_OPTS -jar app.jar"]