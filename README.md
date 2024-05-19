# Event-Driven DDD FastApi Chat

This project is an event-driven chat application built using Domain-Driven Design (DDD) principles. The backend is powered by FastAPI for creating RESTful APIs and handling WebSocket connections, Kafka for message brokering to enable asynchronous communication between different parts of the system, and MongoDB as the primary data store.

The application leverages the mediator pattern to handle commands and events. Commands are executed through the mediator, invoking appropriate handlers which interact with the repositories to perform database operations. Handlers can also produce events that are sent to Kafka. Asyncronous approach is used.

## Project Structure

The project follows a modular structure adhering to DDD principles:

- **api**: Contains FastAPI endpoints and WebSocket handlers.
- **domain**: Contains domain entities, value objects, and domain events.
- **infrastructure**: Contains implementations for repositories and message brokers.
- **logic**: Contains command handlers, event handlers, and mediator implementation.
- **settings**: Configuration settings for the application.
- **tests**: Test cases for the application.
  
## Installation

### Prerequisites

- Python 3.11+
- Docker

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Copy the example environment file and adjust the configurations as needed:
    ```sh
    cp .env.example .env
    ```

3. Install the dependencies using Poetry:
    ```sh
    poetry install
    ```

4. Start the application using Docker Compose and Makefile:
    ```sh
    make all-up
    ```
