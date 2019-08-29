import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

def createInference(category, inferences):
    # Creates Inference in the form of a text, according to the categories and issues
    information = ''
    if category == 0:
        if inferences!={}: information += 'Currently we see issues with ' + \
            ', '.join(inferences.keys())+'.'
        information+=' These features are the ones consuming a lot of power in the appliance. ' + \
                'We suggest you service your appliance as soon as possible or if possible, change your appliance and buy one which contains a Energy Star Rating.'
    elif category == 1:
        if inferences!={}: information += 'Although not major, we see certain issues with ' + \
            ', '.join(inferences.keys())+'.'
        information+= ' We suggest you keep checking for the health and regularly service your appliance.'
    else:
        information += 'Everything looks great! We don\'t see any issues at the moment?'
    return information

def createTipLinks(appliance):
    links = []
    query = "save energy tips " + appliance
    query = query.replace(' ', '+')
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome(chrome_options=options)
    driver.get("https://www.google.com/search?q="+query)
    results = driver.find_elements_by_css_selector('div.r')
    for i in range(3):
        link = results[i].find_element_by_tag_name("a")
        href = link.get_attribute("href")
        links.append(href)
    return links