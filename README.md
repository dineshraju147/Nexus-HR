# Nexus HR

Nexus HR is an advanced AI-powered chatbot designed to streamline and automate HR and administrative tasks. Acting as an intelligent, agentic system, it can understand complex, multi-step commands and use a variety of tools to execute them, significantly reducing manual workload and improving efficiency.

The primary use-case demonstrated is the complete automation of the new employee onboarding process, from creating an HR profile to ordering equipment and scheduling meetings.



## 🚀 Core Features

Nexus HR can perform a wide range of HR-related functions:

* **Automated Employee Onboarding:** A single command like "Onboard new employee John Doe, reporting to Jane Smith" triggers a complete workflow:
    * Adds the new employee to the HRMS.
    * Sends a welcome email with credentials.
    * Notifies the manager.
    * Raises IT tickets for a new laptop and ID card.
    * Schedules an introductory meeting between the employee and their manager.
* **Employee Data Management:**
    * Add new employees.
    * Search for and retrieve employee details by name.
* **IT & Equipment Ticketing:**
    * Create tickets for new equipment (e.g., laptops, ID cards).
    * Update the status of existing tickets.
    * List all tickets for a specific employee.
* **Meeting Management:**
    * Schedule new meetings.
    * View an employee's upcoming meetings.
    * Cancel scheduled meetings.
* **Leave Management:**
    * Check an employee's leave balance.
    * Apply for leave on behalf of an employee.
    * Retrieve an employee's leave history.
* **Communication:**
    * Send emails directly through the chat interface.

## 🛠️ Technical Architecture

The project is built on a client-server architecture, allowing the AI agent to run independently and be accessed from various clients.

* **MCP Client:** The user interacts with the AI through an MCP (Multi-turn Conversation Protocol) client. The current implementation uses the **Claude Desktop** client.
* **MCP Server (`server.py`):** This is the core of the application, built with **FastMCP**. It exposes the AI's capabilities as a set of tools. When the server receives a prompt, the AI reasons about the user's goal, plans a sequence of actions, and calls the appropriate tools to achieve it.
* **Simulated Backend Services:** To function without access to live production systems, Nexus HR uses a set of Python classes that simulate real-world services:
    * **`EmployeeManager`**: A mock HRMS database.
    * **`TicketManager`**: A mock IT helpdesk/ticketing system.
    * **`MeetingManager`**: A mock calendar and scheduling service.
    * **`LeaveManager`**: A mock leave management system.
    * **`emails.py`**: A service for sending emails via SMTP.
* **Data Seeding (`utils.py`):** The simulated services are populated with realistic fake data upon server startup to create a ready-to-use testing environment.

## ⚙️ How It Works: The Onboarding Flow

Nexus HR's agentic nature is best illustrated by the onboarding process:

1.  **User Prompt:** A user issues a high-level command: `Onboard new employee 'Sanjay Kumar' reporting to 'David Wilson'`.
2.  **Goal Recognition:** The AI agent receives this prompt. Guided by the pre-defined `onboard_new_employee` prompt on the server, it understands the final goal and the necessary sub-tasks.
3.  **Tool Selection & Execution:** The agent autonomously executes a series of tools in a logical order:
    * It first calls `get_employee_details` for the manager ('David Wilson') to get their ID.
    * Next, it uses `add_employee` to create a profile for 'Sanjay Kumar' in the HRMS.
    * It then calls `send_email` twice: once to welcome the new employee and again to notify the manager.
    * It proceeds to call `create_ticket` to request a new laptop and ID card.
    * Finally, it calls `schedule_meeting` to put an introductory meeting on the calendar.
4.  **Response:** The agent reports the successful completion of the onboarding process back to the user.

## 🔧 Setup and Running the Server

To run the Nexus HR server locally, follow these steps:

1.  **Prerequisites:**
    * Python 3.8+
    * An MCP client like Claude Desktop.

2.  **Clone the Repository:**
    ```bash
    git clone https://your-repository-url/nexus-hr.git
    cd nexus-hr
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: You will need to create a `requirements.txt` file containing `fastmcp`, `pydantic`, `python-dotenv`, etc.)*

4.  **Environment Variables:**
    Create a `.env` file in the root directory and add your email credentials for the email sending service:
    ```
    CB_GMAIL="your-email@gmail.com"
    CB_GMAIL_PWD="your-app-password"
    ```

5.  **Run the Server:**
    ```bash
    python server.py
    ```

6.  **Connect Client:**
    Once the server is running, connect your MCP client to it to start interacting with Nexus HR.
