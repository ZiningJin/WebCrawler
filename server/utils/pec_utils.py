import time
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ChromeOptions
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, WebDriverException


def pec_util_login(url, username, password):
    browser = webdriver.Edge()
    browser.get(url)

    try:
        WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.NAME, 'loginuser'))).send_keys(username)
        browser.find_element(By.NAME, 'loginpassword').send_keys(password)

        login_button_xpath = ''
        WebDriverWait(browser, 30).until(EC.element_to_be_clickable((By.XPATH, login_button_xpath))).click()
        # Return the browser object for the next step
        return browser

    except Exception as e:
        print("An Error occurred:", e)
        browser.quit()
        return None
    
def pec_util_auth_code(browser, auth_code):
    if browser is None:
        print("Browser is not intialized")
        return
    try:
        authcode_input_xpath = ''
        WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, authcode_input_xpath))).send_keys(auth_code)
        validate_button_xpath = '//*[@id="vCode-btn"]'
        WebDriverWait(browser, 30).until(EC.element_to_be_clickable((By.XPATH, validate_button_xpath))).click()
        # Return the browser object for the next step
        return browser
    except Exception as e:
        print("An error occurred while entering the authentication code:", e)
        browser.quit()
        return None

def pec_util_criteria(browser, start_date_str, end_date_str):
    # Convert the start and end dates to the required format: '23-Jan-2024'
    if browser is None:
        print("Browser is not initialized")
        return

    try:
        # Click various criteria 
        capital_click_xpath = '/'
        newProjects_click_xpath = ''
        projectStatusActive_click_xpath = ''
        projectStatusUnconfirmed_click_xpath = ''
        worldregion_click_xpath = ''
        traderegion_click_xpath = ''


        WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, capital_click_xpath))).click()
        WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, newProjects_click_xpath))).click()
        WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, projectStatusActive_click_xpath))).click()
        WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, projectStatusUnconfirmed_click_xpath))).click()
        WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, worldregion_click_xpath))).click()
        WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, traderegion_click_xpath))).click()
        
        projectindustry_xpath_dict = {
            'power':'',
            'productOG':'',
            'alternativefuel':'',
            'petrolrefine': '',
            'chemicalprocess': '',
            'foodandbever': '',
            'metalandmineral': '',
            'industryandmanufacture': '',
            'pulpandpaper': '',
            'pharandmedical': ''
        }

        for i in projectindustry_xpath_dict.keys():
            WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, projectindustry_xpath_dict[i]))).click()
        
        # Set the date filters using JavaScript
        browser.execute_script('document.getElementsByClassName("datepicker_dMY form-control input-xs ui-corner-all")[0].value=arguments[0];', start_date_str)
        browser.execute_script('document.getElementsByClassName("datepicker_dMY form-control input-xs ui-corner-all")[1].value=arguments[0];', end_date_str)

        # click the 'run query' button
        run_query_button_xpath = ''
        WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, run_query_button_xpath))).click()
        
        # Return the browser object for the next step
        return browser
    
    except NoSuchElementException as e:
        print(f"Error: Element not found - {e}")
        return None
    except WebDriverException as e:
        print(f"Webdriver Error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def pec_util_extract(browser):
    if browser is None:
        print("Browser not passed the set criteria step")
        return

    projectINFOs = {}
    current_page = 1
    try:
        
        '''
        EXTRACT projectIDs
        1. Determine the number of pages
        2. Loop through pages and extract projectIDs/projectURL/countryZone
        3. return list projectIDs and dict projectINFOs
        '''
        while True:
            # Determine the number of rows on the current page
            rows = browser.find_elements(By.XPATH, '//*[@id="DataTables_Table_0"]/tbody/tr')
            num_rows = len(rows)
            for i in range(1, num_rows, 2):
                # extact projectID, projectURL, countryZone
                projectID_xpath = f'//*[@id="DataTables_Table_0"]/tbody/tr[{i}]/td[4]'
                projectIndustry_xpath = f''
                countryZone_xpath = f''

                projectID = browser.find_element(By.XPATH, projectID_xpath).text
                projectIndustry = browser.find_element(By.XPATH, projectIndustry_xpath).text
                countryZone = browser.find_element(By.XPATH, countryZone_xpath).text

                projectURL = f'https://www.industrialinfo.com/dash/project_report.jsp?PROJECT_ID={projectID}&setFilter='
                projectINFOs[projectID] = {'URL': projectURL, 'Industry': projectIndustry, 'countryZone': countryZone}
            print(f'------ Finish the for loop of {current_page}-th page ------')
                
            
            # Check if there are more pages to turnover
            pagination_elements = browser.find_elements(By.XPATH, '//*[@id="paginationContent"]/a')
            if current_page >= len(pagination_elements):
                break

            # Click to turnover the page
            next_page_btn = pagination_elements[current_page]
            next_page_btn.click()
            current_page += 1
            time.sleep(3)
        
        ''' 
        EXTRACT DETAILS
        1. take projectIDs and projectINFOs from revious
        2. extract project details
        3. return complete projectINFOs for data transformation
        '''
        for projectID in projectINFOs:
            # open projectURL
            browser.get(projectINFOs[projectID]['URL'])

            # Extract projectName
            try:
                projectName = browser.find_element(By.XPATH, "").text
            except NoSuchElementException:
                XXX = None
            projectINFOs[projectID]['projectName'] = projectName

            # Extract projectType
            try:
                projectType  = browser.find_element(By.XPATH, "").text
            except NoSuchElementException:
                projectType  = None
            projectINFOs[projectID]['projectType '] = projectType

            # Extract plantOwner
            try:
                plantOwner = browser.find_element(By.XPATH, "").text
            except NoSuchElementException:
                plantOwner = None
            projectINFOs[projectID]['plantOwner'] = plantOwner

            # Extract location
            try:
                location = browser.find_element(By.XPATH, "").text
            except NoSuchElementException:
                location = None
            projectINFOs[projectID]['location'] = location

            # Extract cityState
            cityState = None
            for cityState_title in ['City/State','Field Name/Water Body']:
                try:
                    cityState = browser.find_element(By.XPATH, f"").text
                    break
                except NoSuchElementException:
                    continue
            projectINFOs[projectID]['cityState'] = cityState

            # Extract fullContacts
            fullContacts = None
            for contact_title in ['Project Manager', 'Project Executive', 'Project Director']:
                try:
                    fullContacts1 = browser.find_element(By.XPATH, f"//b[text()='{contact_title}']/../../following-sibling::td[1]").text 
                    fullContacts2 = browser.find_element(By.XPATH, f"").text 
                    fullContacts3 = browser.find_element(By.XPATH, f"").text 
                    fullContacts4 = browser.find_element(By.XPATH, f"").text 
                    fullContacts5 = browser.find_element(By.XPATH, f"").text 
                    fullContacts6 = browser.find_element(By.XPATH, f"").text 
                    fullContacts7 = browser.find_element(By.XPATH, f"]").text 
                    fullContacts = 'Project Manager:'+fullContacts1+fullContacts2+';'+fullContacts3+fullContacts4+';'+fullContacts5+fullContacts6+fullContacts7
                    break
                except NoSuchElementException:
                    continue
            projectINFOs[projectID]['fullContacts'] = fullContacts

            # Extract scope
            try:
                scope = browser.find_element(By.XPATH, "").text
            except NoSuchElementException:
                scope = None
            projectINFOs[projectID]['scope'] = scope

            # Extract schedule
            try:
                schedule = browser.find_element(By.XPATH, "").text
            except NoSuchElementException:
                schedule = None
            projectINFOs[projectID]['schedule'] = schedule

        # Extract contactName
            try:
                contactName = browser.find_element(By.XPATH, "").text
            except NoSuchElementException:
                contactName = None
            projectINFOs[projectID]['contactName'] = contactName

        # Extract contactPhone
            try:
                contactPhone = browser.find_element(By.XPATH, "").text
            except NoSuchElementException:
                contactPhone = None
            projectINFOs[projectID]['contactPhone'] = contactPhone
    
    except Exception as e:
        print(f"An error occurred: {e}")
        
    finally:
        browser.quit()

    return projectINFOs

def pec_util_email(x):
    pat1 = 'E-Mail\]([\s\S]*)'
    if re.findall(pat1, x) != []:
        return re.findall(pat1, x)[0]
    else:
        return None

def pec_util_transform(projectINFOs):
    df =  pd.DataFrame.from_dict(projectINFOs, orient='index')
    df = df.reset_index().rename(columns={
        'index':'External ID',
        'projectName':'Project Name',
        'contactName':'Last Name',
        'contactPhone':'Phone',
        'plantOwner':'Company', 
        'fullContacts':'Owner Enterprise'})
    
    df['WG_AMT'] = 'WG'
    df['Brands'] = 'Ingersoll Rand'
    df['Product Category'] = 'Compressor'
    df['Lead Source'] = 'Project Database'
    df['Lead Source 1'] = 'PEC'

    df['Project Description'] = df['scope']+df['schedule']
    df['Project Address'] = df['location'].map(str) + df['cityState'].map(str)

    df['Country'] = df['countryZone'].apply(lambda x: x.split(' ')[0])
    df['Country'] = df['Country'].apply(lambda x: 'Viet Nam' if x=='Vietnam' else x)

    df['Email Address'] = df['Owner Enterprise'].apply(lambda x: pec_util_email(x.split(';')[1]))
    df['Email Address'] = df['Email Address'].apply(lambda x: x.strip() if x != None else x)

    df['Phone'] = df['Phone'].apply(lambda x: x.split('/')[0])
    df['Phone'] = df['Phone'].apply(lambda x: x.strip('[Phn.] '))

    df['Marketing_ID'] = "" 
    df['State'] = ""
    df['City'] = "" 
    df['Lead Source 2'] = "" 
    df['Lead Source 3'] = "" 
    df['Lead Source 4'] = ""
    df['Start Time'] = "" 
    df['Project Stage 1'] = "" 
    df['Project Property'] = ""
    df['Design Enterprise'] = "" 
    df['EPC Enterprise'] = ""

    df = df[['Project Name','External ID','Marketing_ID','Last Name', 'Phone','Email Address','WG_AMT', 'Brands',
        'Product Category','Country','State', 'City','Industry','Lead Source','Lead Source 1','Lead Source 2',
        'Lead Source 3', 'Lead Source 4', 'Start Time','Company','Project Description','Project Stage 1',
        'Project Property','Project Address','Owner Enterprise','Design Enterprise', 'EPC Enterprise']]

    return df
