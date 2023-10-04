Changelog
=========

0.1.0-alpha (2023-09-01)

------------------
Added:

- Command line configuration module
- User/Repo information query
- Metrics query and filtering for user/repo
- Display of user/repo metrics on the command line (table | histogram | heat map)
- Exporting user/repo metrics to a JSON file
- Plugin support

0.2.0-alpha (2023-09-04)

------------------
Added:

- export indicator data to echarts report

Fixed:

- fix failed query in project openrank network indicator

1.0.0 (2023-10-04)

------------------
Added:

- Add the ability to print levels data in the terminal.
- add datetime in filename
- Make error alerts clearer
- add create_issue api
- create no data issue automatically
- use gpt3.5 to analyze data

Fixed:

- Fix printing detailed indicators twice
- Fix activity data inconsistency with official issues
- Fix missing a judgment when parsing time ranges
- Fixing the effects of '-raw'
- Fix OOM error
- Fix chart export for Activity and ActivityDetail
- Fix json format exported by json exporter
- Fix a literal error
