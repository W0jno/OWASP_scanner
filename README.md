# OWASP Scanner 🛡️

**OWASP Scanner** is a full-stack (frontend + backend + database) web application security analysis tool, built with the OWASP Top 10 in mind. It allows for automated scanning of web apps and presents the results in an interactive dashboard.

---

## 🧩 Table of Contents

1. [Features](#features)  
2. [Project Architecture](#project-architecture)  
3. [Technologies](#technologies)  
4. [Installation & Running](#installation--running)  
5. [Usage](#usage)  

---

## Features

- Automatically scans web applications for vulnerabilities based on the **OWASP Top 10**.  
- Modern and interactive web interface for reviewing scan results.  
- Stores scan history in a persistent database.  

---

## Project Architecture

This project is structured into three main components:

- **frontend/** – web UI built using TypeScript, HTML, and CSS.  
- **backend/** – API and scan logic written in Python.  
- **db/** – database configuration and migrations.

Everything is orchestrated using `docker-compose.yml` for quick setup and deployment using containers.

---

## Technologies

- **Python** – backend logic and APIs  
- **TypeScript**, **HTML**, **CSS** – frontend user interface  
- **SQL** (e.g., PostgreSQL or SQLite) – database  
- **Docker & Docker Compose** – containerization  
- **OWASP Top 10** – security scanning standards

---

## Installation & Running

1. Clone the repository:

    ```bash
    git clone https://github.com/W0jno/OWASP_scanner.git
    cd OWASP_scanner
    ```

2. Make sure you have Docker and Docker Compose installed.

3. Start the project:

    For backed and database use:
    ```bash
    docker-compose up --build
    ```

   This will start: 
   - The backend API  
   - The database
  
    For frontend go to the /fronted folder, then:

   ```bash
   npm run dev
   ```

   This will start:
   - The frontend

5. After startup:
   - Frontend available at: `http://localhost:3000`  
   - Backend API at: `http://localhost:8000`

6. (Optional) You can customize the configuration in `docker-compose.yml`, including ports and environment variables.

---

## Usage

1. Open your browser and go to `http://localhost:3000`.  
2. Enter the URL of the web application to be scanned.  
3. Wait for the scan to complete.  
4. View and explore the results in the dashboard.   
5. All scans are stored in the database for future access.


---

## Contact

For questions, suggestions, or feedback, feel free to reach out at: **filip.wojno03@gmail.com**

---

**OWASP Scanner** is a robust tool for quickly identifying web application vulnerabilities. Built with simplicity, extensibility, and security best practices in mind.  

Enjoy scanning — and stay secure!

---

*Made with ❤️ by W0jno.*
