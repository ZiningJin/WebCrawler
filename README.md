# WebCrawler
## Main Function: A Toolbox designed for project database leads automation 
## Project Databases:
- [BCI Centrial](https://app-leadmanager.bcicentral.com/main/dashboard)
- [PEC Industrial](https://www.industrialinfo.com/)
- [CCEUP](http://www.cceup.com/)

## Previous Manual Workflow
- Step1: Set Criteria (industry category; company type; region; start date; end date, etc.)
- Step2: manually copy and paste each project's information from the project database website (**LOW EFFICIENCY**)
- Step3: transform into Salesforce Leads Module required format (**HEAVY EXCEL WORK**)

## New Workflow
- Step1: No need for manual setups
- Step2: No need for manual crawling work
- Step3: No need for manual data transformation
  Check the workflows for each project database:
  ![workflows](https://github.com/ZiningJin/WebCrawler/blob/main/workflows.png)

  ## Tech Stack
  > Frontend: React.js (react-bootstrap), Axios
  > Backend: Flask (selenium for browser state management)
  > Database: MySQL (pymysql, SQLAlchemy)
  > Test Tool: POSTMAN
