# Planning

The program provides a calendar for visualizing important time sensitive information.
In particular it's responsible for showing planning information regarding:
- Run Schedules
- Planned maintenance events

### Calendar

The calendar can be viewed in 4 different modes
- Month view
- Week view
- Day view
- Gantt view

The last view is helpful for viewing events that span multiple days.
To navigate between views, use the buttons labelled on the top right of the page. To view previous and next groups of data within the same view, use the arrow buttons on the top right of the page.

In the month and week views, clicking on a date number will bring up the day view for the selected content.


### Run Schedules

Run Schedules are used to track for a given period, how many hours a machine is meant to run and for how many day over a given week. It is indicated by a start and end date, as well as run hours and checkboxes for each day of the week the machine is expected to run.

The schedules can then be viewed in the calendar, with each machine running on a given date as being listed on it. The schedule can also be viewed in the machine entity itself providing a scoped view of the planned run for the machine.

Within a run schedule are orders. An order can be recorded in the system and listed under the machine dashboard or the run plan dashboard if the order falls within the range of dates of the schedule.


### Planned Maintenance

The calendar also tracks planned maintenance events, namely preventative tasks and checklists. All such tasks are rendered on the calendar view according to their schedules
