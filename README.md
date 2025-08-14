# Cookie-Tossing (Cookie Counterfeiting) Lab 

This lab was developed to learn and exploit cookie tossing with the help of stored XSS vulnerability within a blog domain.
The idea for this lab comes from Tom Anthony's Nahamcon 2025 talk regarding XSS vulnerabilties being leveraged to a high or critical vulnerability using this method.

## Project Structure

```
Cookie-Tossing/
├── cookie-tossing.lab:8083/         # Main web application that has user registration and log in page and /credit-card where will be used to exfiltrate user's info
├── blog.cookie-tossing.lab:8084/         # Blog paste that has stored XSS vulnerability
└── docker-compose.yml
```

## Prerequisites

- Docker
- Docker Compose

## Getting Started

1. Clone this repository
2. Run the environment:
   ```bash
   docker-compose up --build
   ```
3. Go to /etc/hosts and set 127.0.0.1 or machine IP that is running docker containers to resolve **cookie-tossing.lab** and **blog.cookie-tossing.lab**
4. Access the main web application at `http://cookie-tossing.lab:8083`
5. The blog page will be running at `http://blog.cookie-tossing.lab:8084`

## Security Notice

This lab is designed for educational purposes only. Both web applications intentionally contain vulnerabilities related to Cross-Site Scripting and Cookie Tossing. Do not deploy this in a production environment. 