# STACK-BUILDER

![res](https://gitlab.com/internship4450447/informatiako/-/raw/main/stack_builder/resources/_30ae5a5d-bc48-4193-8347-b1014009271c.jpg)

## Table of Contents
- [Getting Started](#getting-started)
  - [What is it?](#what-is-it)
  - [Requirements](#requirements)
  - [Setup](#setup)
  - [Installation](#installation)
  - [Create Your First Socle](#create-your-first-socle)
- [why use stack-builder?](#why-use-stack-builder)
- [LICENSE](#license)

---

## Getting Started
If you are new to **Stack-Builder**, this section will guide you through the essential resources to get started.

### What is it?
**Stack-Builder** is an open-source Python package designed to simplify the creation of project foundations (socles). With Stack-Builder, you can easily generate Dockerfiles, Docker Compose configurations, set up database settings, and much more—all with a single command.

### Requirements
- **Python**: Since Stack-Builder is a Python package, you need to install Python. The recommended version is **3.11** or newer.
- **Docker CLI**: Docker is essential for managing various technologies and their versions efficiently. It resolves compatibility issues that arise when using multiple technologies.

### Setup

#### Step 1: Install Python (Version 3.11 or newer)
- Visit the [official Python website](https://www.python.org/downloads/) to download and install Python for your system.

#### Step 2: Install Docker
- Go to the [official Docker website](https://www.docker.com/) and select the appropriate version for your system.

#### Step 3: Create a Virtual Environment with Python and Activate It

For **Unix/macOS**:
```bash
python3 -m venv .env_stack_builder
source .env_stack_builder/bin/activate                
```

For **Windows**:
```powershell
py -m venv .env_stack_builder
.env_stack_builder\Scripts\activate
```

#### Step 4: Start Docker
Ensure Docker is running before proceeding.

---

### Installation
Install the Stack-Builder package using `pip`:

For **Unix/macOS**:
```bash
python -m pip install stack-builder
```

For **Windows**:
```powershell
py -m pip install stack-builder
```

---

### Create Your First Socle

Here is an example of creating a project foundation with **Django** and **PostgreSQL** as the database. Note that the initial creation of the Django project requires an active internet connection.

Run the following command (works for both Bash and PowerShell) [config.yaml](https://gitlab.com/internship4450447/informatiako/-/raw/main/stack_builder/source_code/config.yaml?ref_type=heads):
```bash
stack-builder --config config.yaml
```


This command will:
- Create a Django application.
- Configure PostgreSQL as the database.
- Set up Dockerfiles and Docker Compose configurations for your project.

---

## why use stack-builder?

*   [x] **Easy to use** like speak.

*   [x] **gain tima** for fast template.

*   [x] **open source** to keep users consient of project mechanism.



## LICENSE

[MIT](https://gitlab.com/internship4450447/informatiako/-/raw/main/LICENSE?ref_type=heads)

Enjoy building your project with Stack-Builder! 🚀

