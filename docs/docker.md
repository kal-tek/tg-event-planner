## 🐳 Docker Integration

Docker provides an efficient, lightweight approach to application deployment by creating containerized versions of applications. This ensures consistency across various environments, eliminating the "it works on my machine" syndrome.

### Building the Docker Image

1. **Image Creation**:
   Navigate to the project's root directory and use the following command to build a Docker image for your application:

   ```bash
   docker build -f docker/dev.Dockerfile -t event-planner .
   ```

### Running the Docker Container

1. **Run Container**:
   With the image built, start a container instance of your application:

   ```bash
   docker run --env-file=.env -p 8000:8000 event-planner
   ```

   This will expose the application on port 8000. Adjust the port mappings as required.

### Docker Compose Integration

`docker-compose` streamlines multi-container Docker applications' management, such as when running both a web server and a database.

1. **Run Services**:
   Use the following command to start your services (e.g., server and database):

   ```bash
   docker-compose up
   ```

   This will start both the server and the database, as defined in the `docker-compose.yml` file.

2. **Shutdown Services**:
   To gracefully stop your services, use:

   ```bash
   docker-compose down
   ```

With Docker and `docker-compose` in place, you can reliably run and manage your application across different environments with ease.
