---
name: docker
description: Docker and Docker Compose operations on this VPS. Use when managing containers, running docker compose, monitoring container status, viewing logs, or troubleshooting Docker-related issues. This skill provides guidance for common Docker workflows including running compose, checking container health, viewing logs, and understanding Docker operations on this server.
---

# Docker Skill

## When to Use This Skill

Use this skill whenever you need to:
- Run `docker compose up`, `docker compose down`, or other compose commands
- Check container status and health
- View and analyze container logs
- Troubleshoot Docker issues (build failures, hanging operations, etc.)
- Manage Docker operations on this VPS

## Quick Reference

### Basic Commands

```bash
# Check running containers
docker ps

# Check all containers (including stopped)
docker ps -a

# View logs for a container
docker logs <container-name> -f

# Docker Compose operations
docker compose up -d        # Start in detached mode
docker compose down         # Stop and remove containers
docker compose logs -f      # Follow logs
docker compose ps           # Show container status
docker compose top          # Show running processes
```

## Important Considerations

### Long-Running Operations

Docker operations can take significant time, especially:
- **Building images**: First-time builds can take 5-30+ minutes
- **Exporting layers**: `=> => exporting layers` is a normal build phase that can take several minutes
- **Large images**: Heavy services (databases, ML models) build slower

**Don't panic if operations appear "stuck"** - check logs and actual progress before assuming failure.

### Monitoring Long Operations

When running long Docker operations:

1. **Use background mode** (`-d` flag) for compose when possible
2. **Monitor logs** with `docker compose logs -f` or `docker logs <container> -f`
3. **Check container status** periodically with `docker ps` or `docker compose ps`
4. **Look for actual errors** - not just silence

### Checking Container Health

```bash
# Basic status
docker compose ps

# Detailed status with health
docker inspect <container-id> | grep -A 10 Health

# Recent logs (last 50 lines)
docker logs <container-name> --tail 50

# Follow logs in real-time
docker logs <container-name> -f
```

## Troubleshooting

### Build Appears Stuck

1. Check if it's still running:
   ```bash
   docker ps
   ```

2. View build logs:
   ```bash
   docker compose logs -f
   ```

3. Check disk space:
   ```bash
   df -h
   docker system df
   ```

### Container Won't Start

1. View logs for the specific service:
   ```bash
   docker compose logs <service-name>
   ```

2. Check for port conflicts:
   ```bash
   netstat -tulpn | grep <port>
   ```

3. Verify docker-compose.yml syntax:
   ```bash
   docker compose config
   ```

### Common Build Phases

When seeing build output, understand these are normal phases:
- `[+] Building` - Overall build in progress
- `=> => pulling image` - Downloading base images
- `=> => sending context` - Preparing build context
- `=> => exporting to image` - Saving built image (can take 5-10+ minutes)

**Note**: Long pauses during `exporting to image` are normal, not errors.

## This Server's Docker Setup

### Docker Compose Location

Docker Compose projects are typically located in their respective project directories. Always navigate to the project directory before running compose commands.

### Common Projects

Projects managed on this server include:
- Various agent/memory-related projects in `/root/.openclaw/workspace/` or subdirectories

### Best Practices

1. **Always use `docker compose` (v2)**, not `docker-compose` (v1)
2. **Run in detached mode** (`-d`) for background services
3. **Check logs before assuming failure** - Docker can be slow
4. **Use `docker compose ps`** to verify container status after operations
5. **Clean up unused resources** periodically:
   ```bash
   docker system prune -a    # Remove unused containers, networks, images
   docker volume prune        # Remove unused volumes
   ```

## Error Handling

If you encounter Docker errors:

1. **Read the full error message** - Docker provides detailed error info
2. **Check logs** for the specific container or service
3. **Verify resources** (disk space, memory, ports)
4. **Search for the specific error** if it's not clear
5. **Ask the user** before attempting destructive operations (e.g., `docker system prune -a`)
