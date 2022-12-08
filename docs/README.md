## Features
Plantlink is a suite of tools for planned maintenance and breakdown maintenance. Additionally, it provides features for organizing machinery into a tree of components. Plantlink also implements reporting based on data captured by users.

- Inventory Management. The application provides a 5 tier structure for representing machinery in a plant. A machine is divided into sections, which are then divided into subunits which are further divided into subassemblies and finally divided into components. These machines can be explored in a tree interface and maintenance activities can be scoped at a granular level of detail as a result. Plantlink also tracks spares. It tracks what spares were used in maintenance and what spares are held in stock associated with a given machine. Both machinery and spares can be imported directly from excel into the application by means of a template.
- Breakdown Maintenance. Plantlink implements a model for work orders which represents unplanned jobs performed on equipment. The jobs track resolvers, spares and downtime.
- Planned Maintenance. Planned jobs are modelled as preventative tasks in the system. Similar to unplanned jobs, assigned resolvers, spares and planned downtime can be recorded and the data captured is incorporated into reporting. Planned jobs appear in the maintenance calendar as well as the inboxes of maintenance personnel. In addition to preventative tasks, Plantlink has a Checklist model, that can be used to schedule machine inspections at regular intervals. 
- Production Planning Plantlink has a simplified calendar that can shows the running schedules for various machines as well as the planned maintenance for each. This visibility enables teams to avoid scheduling conflicts and predict downtime.
- Reporting. Plantlink comes with 6 reports:
    1. Spares requirements - a forecast of required spares based on planned jobs.
    2. Spares usage - a summary of spares used over a given period
    3. Breakdown summary - a brief history of breakdowns over a period and the downtime associated with them
    4. Maintenance review - a comparison between a mainteance plan and the actual maintenance tasks undertaken over a given period
    5. Maintenance plan - a summary of preventative tasks that will be undertaken in the future
    6. Weak point analysis - Identifies areas and components of a machine with the highest frequency of breakdowns.


## Installation
1. Install Python version 3.6 or later
2. Install git
3. Install wkhtmltopdf 
    - Download it from here `https://wkhtmltopdf.org/`
    - Add the bin/ folder to the system path 
4. Clone the project
    `git clone https://github.com/nakamura9/plantlink_v2`
5. Create a virtual environment for the project and activate it.
    `python -m venv env`
    `env/scripts/activate`
6. Install the project dependencies 
    `cd plantlink_v2`
    `pip install -r requirements.txt`
7. Run database migrations
    `python manage.py migrate`
8. Create a superuser 
    `python manage.py createsuperuser`
    Follow the prompts to create the admin account
9. Install the reports 
    `python manage.py loaddata reports.json`
## Usage

1. To run the application server, enter the following command in the plantlink_v2 directory.
`python manage.py runserver`
2. Launch the application from the browser at the address localhost:8000/login
3. 
