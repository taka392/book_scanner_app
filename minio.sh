#!/bin/bash

# Docker環境の管理スクリプト

set -e

COMPOSE_FILE="docker-compose.minio.yml"

case "$1" in
  start)
    echo "Starting services..."
    docker-compose -f $COMPOSE_FILE up -d --build
    echo "Services started successfully!"
    echo "MinIO API: http://localhost:9000"
    echo "MinIO Console: http://localhost:9001"
    echo "BFF: http://localhost:8080"
    echo "Backend: http://localhost:8000"
    echo "PostgreSQL: localhost:5432"
    echo "Username: minio"
    echo "Password: dev-password"
    ;;
  
  stop)
    echo "Stopping MinIO..."
    docker-compose -f $COMPOSE_FILE down
    echo "MinIO stopped successfully!"
    ;;
  
  restart)
    echo "Restarting MinIO..."
    docker-compose -f $COMPOSE_FILE down
    docker-compose -f $COMPOSE_FILE up -d
    echo "MinIO restarted successfully!"
    ;;
  
  logs)
    echo "Showing MinIO logs..."
    docker-compose -f $COMPOSE_FILE logs -f
    ;;
  
  status)
    echo "MinIO container status:"
    docker-compose -f $COMPOSE_FILE ps
    ;;
  
  clean)
    echo "Cleaning up MinIO (WARNING: This will delete all data)..."
    read -p "Are you sure? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
      docker-compose -f $COMPOSE_FILE down -v
      docker volume rm book_scanner_app_minio_data 2>/dev/null || true
      echo "MinIO cleanup completed!"
    else
      echo "Cleanup cancelled."
    fi
    ;;
  
  *)
    echo "Usage: $0 {start|stop|restart|logs|status|clean}"
    echo "  start   - Start MinIO services"
    echo "  stop    - Stop MinIO services"
    echo "  restart - Restart MinIO services"
    echo "  logs    - Show MinIO logs"
    echo "  status  - Show container status"
    echo "  clean   - Clean up all MinIO data (WARNING: destructive)"
    exit 1
    ;;
esac
