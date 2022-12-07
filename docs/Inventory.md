#Inventory 

### Data Imports

The program supports importing inventory from an excel spreadsheet. 

A sample file is included with this documentation. The file consists of two columns:
- Part ID
- Part Name

The part ID determines which level of invetory a part occupies. 2 digits indicates a machine, 4 a section and so forth up to 10, which represents a component. When properly formatted, the spreadsheet will load all the parts in the appropriate hierarchy automatically. 

NB: Please note that machines cannot be imported automatically and must be assigned a code in the system first before its components can be added.

To import a file, navigate to the home page for the inventory app /app/inventory and use the file selector widget on the right to select the file you want to support. Please make sure it's a valid .xlsx file or a valid .csv file. Once selected, use the dropdown below to select 'Machines' as the import type, then click the blue button labelled 'Import'.

NB Imports can only work on a production server with support for background jobs

### 5 Levels of machine inventory

The program divides inventory into 5 Levels. Listed below from top to bottom:
- Machines
- Sections
- Subunits
- Subassemblies
- Components

Each inventory type is linked to its ancestors and children so that they can be viewed hierarchically using the sidebar on the left of the form for each level. Opening the form of a machine for instance will list the count of its descendants on the left and a tree widget for exploring each element.
Maintenance can be drilled down to the exact component of a machine for root cause analysis and reporting purposes.

There are special views for machines. Clicking on a machine in the machine list view, will bring up a dashboard that in addition to rendering the hierarchy of components, shows a maintenance history of the machine, listing the most recent breakdowns and the upcoming planned maintenance for the machine. It also states the recent run history of the machine.

Sections, Subunits and Subassemblies have a similarly configured detail view, showing both breakdown and planned maintenance.  

### Assets

Assets are documents linked to machines and record accounting data, at the moment the model is quite sparse without much detail.

### Items

Items are spares objects recorded in the system that link up with components and are used in maintenance tasks. The program keeps track of what quantity of spares are available for maintenance purposes and their consumption over time.

### Plants 

Plants exist to divide related machines into groups, for instance main plant vs sheet plant.
