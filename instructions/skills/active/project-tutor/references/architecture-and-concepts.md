# Architecture and Concepts

## Detecting Tech Stack
When asked to analyze a project, look for key configuration files to guess the tech stack:
- `package.json`: Node.js, React, Angular, Vue.
- `pom.xml` / `build.gradle`: Java Spring Boot.
- `requirements.txt` / `Pipfile` / `pyproject.toml`: Python (Django, Flask, FastAPI).
- `go.mod`: Golang.
- `Dockerfile` / `docker-compose.yml`: Containerized setup.

## Explaining Architecture
Focus on **interaction mechanisms** and how components connect. Do not use the Feynman method (analogies) unless the system is highly abstract.

### MVC (Model-View-Controller)
- **Interaction Mechanism**: 
  - The **Controller** receives the incoming HTTP request, parses the parameters, and decides what needs to be done.
  - It then calls the **Model** to fetch or update data in the database.
  - Once the Model returns the data, the Controller passes it to the **View**, which renders the final HTML (or JSON) to send back to the user.

### Microservices
- **Interaction Mechanism**: 
  - Instead of direct function calls within the same codebase, independent services run on different ports or servers.
  - They connect and interact with each other via network protocols (like REST APIs, gRPC) or message brokers (like RabbitMQ, Kafka).

### Layered Architecture
- **Interaction Mechanism**: 
  - A strict top-down communication flow. 
  - The **Presentation Layer** (e.g., Controllers) can only call the **Business Layer** (e.g., Services).
  - The **Business Layer** contains the core logic and calls the **Data Layer** (e.g., Repositories) to read/write to the database.

## Explaining Common Jargon
Whenever you encounter jargon in the codebase, proactively define it by explaining its role in the connection flow.
- **ORM (Object-Relational Mapping)**: The connection layer between the application code and the database. It converts rows from a SQL table directly into code objects so the Business layer can interact with them easily.
- **API (Application Programming Interface)**: The defined contract or interface that allows two separate systems (like a React frontend and a Node.js backend) to communicate with each other over HTTP.
- **Middleware**: A function that sits in the middle of the request-response cycle. It intercepts the incoming request to perform checks (like validating a token) before passing it along to the final Controller.
