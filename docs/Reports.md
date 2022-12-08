### Reports

The program implements 6 reports.
Each report supports filters depending on the data rendered, exporting to PDF or viewing in the browser.
Reports are composed of charts, tables and data designed to provide insight into the maintenance process.

#### Maintenance Review

The maintenance review is report designed to give a high level overview of maintenance actions and their impact on machine availability for a given range of dates and for a particular machine or all machines. The report begins with a 3 statement summary, outlining the scope of the report - the dates covered and the machines included. 
The final statement indicates the number of breakdowns and the total downtime.

The next section of the report indicates the planned maintenance undertaken, the preventative tasks and checklists and the time taken for each.

Following this is the breakdowns over the period providing a summary in tabular form of the breakdowns that occurred over the period.

Finally there's a charts section which renders a bar chart for the machine availability as a percentage over discrete dates or ranges of dates over a given period, depending on the scope of the report.

#### Maintenance Plan

The maintenance plan is a report that outlines all the upcoming maintenance activities. It contains 2 tables with checklists and preventative tasks. 

It can be customized with filters to show only the tasks for a certain period or a given machine. 

#### Breakdown Analysis

Breakdown analysis provides a detailed account of breakdowns for a specific period and for specific machines. 

It starts with a summary outlining the scope of the report that follows, the dates covered and the machines included. It then concludes with a summary of the number of breakdowns and the total downtime.

The next section is a table of breakdowns listing the machine, problem, duration and corrective action.

Following this is a number of maintenance related charts:
1. Breakdown count by machine, comparing which machines are most unreliable.
2. Breakdown hours by machine, comparing which breakdowns are most severe
3. Breakdown hours by time interval, the trend over time of breakdowns for all machines
4. Breakdown maintenance vs planned maintenance, used to identify machines that receive insufficient planned maintenance compared to their breakdown maintenance.

#### Spares Requirements

This is a simple report listing the number of unique spares items required for all the preventative tasks for a given period. 
It lists the spares by stock ID, available quantity as well as the preventative task the spares will be used for and the date the task will be undertaken.


#### Spares Usage

The spares usage report is a review of spares used in maintenance activities in the system within the scope of dates and selected machinery. 

#### Weak Point Analysis

Weak point analysis is designed to identify problem areas in equipment that need to be addressed. It does so by showing the frequency and severity of breakdowns in the plant. 

The summary at the top of the report is particularly detailed, In addition to listing the scope of the report, it also states how the breakdowns are classified. It states the machine with the highest frequency of breakdowns, the section of the machine with the most breakdowns and the most unreliable component. 
It provides this summary both by count, that is the number of breakdowns and by severity, that is the duration of breakdowns. 


THe report then provides a table of breakdown events over the scope of the report. 

Finally the report has 3 charts each of which is a duration vs count listing of breakdowns for:
1. Machines,
2. Sections
3. And Components