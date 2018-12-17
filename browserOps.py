from selenium import webdriver
import time

# Boot up webdriver (Firefox)
driver = webdriver.Firefox()

def process_cart(url):
    # Boot up webdriver; process adidas url
    driver.get(url)
    # Get initial amount of items in bag
    items_in_bag = driver.find_element_by_css_selector('.glass_cart_count___1UWuC').text
    # If bag is empty, assign valid int value
    if items_in_bag == '':
        items_in_bag = 0
    # Cast temp, initialize constant
    items_in_bag = int(items_in_bag)
    UPDATED = items_in_bag + 1
    # Grab CSS to "Add to Bag" button
    btn = driver.find_element_by_css_selector('.gl-cta.gl-cta--primary.gl-cta--full-width.btn-bag')
    # While bag has not updated, add to bag
    while items_in_bag != UPDATED:
        btn.click()
        items_in_bag = driver.find_element_by_css_selector('.glass_cart_count___1UWuC').text
        if items_in_bag == '':
            items_in_bag = 0
        items_in_bag = int(items_in_bag)
    # Allocate time to process item bagging (avoid unexpected error pg.)
    time.sleep(2)
    # Navigate to Checkout page
    driver.get('https://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/Cart-Show')
    # FWD to CardInfo page
    btn = driver.find_element_by_css_selector('.gl-cta.gl-cta--primary.gl-cta--full-width')
    btn.click()

def autofill_shipping():
    # Read client info from file
    with open('ClientInfo.txt','r') as file:
        #Autofill information
        driver.find_element_by_id('dwfrm_shipping_shiptoaddress_shippingAddress_firstName').send_keys(file.readline())
        driver.find_element_by_id('dwfrm_shipping_shiptoaddress_shippingAddress_lastName').send_keys(file.readline())
        driver.find_element_by_id('dwfrm_shipping_shiptoaddress_shippingAddress_address1').send_keys(file.readline())
        driver.find_element_by_id('dwfrm_shipping_shiptoaddress_shippingAddress_city').send_keys(file.readline())
        s = (file.readline()).replace('\n','')
        driver.find_element_by_id('dwfrm_shipping_shiptoaddress_shippingAddress_postalCode').send_keys(file.readline())
        driver.find_element_by_id('dwfrm_shipping_shiptoaddress_shippingAddress_phone').send_keys(file.readline())
        driver.find_element_by_id('dwfrm_shipping_email_emailAddress').send_keys(file.readline())
    # Select state
    driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/div/div/div[2]/form/div[1]/ng-form/div[1]/div/div[6]/div[1]/div[1]').click()
    list = driver.find_elements_by_class_name('materialize-select-list.dwfrm_shipping_shiptoaddress_shippingAddress_countyProvince')
    states = list[0].find_elements_by_css_selector('*')
    # Select state
    for state in states:
        if state.text == s:
            state.click()
    # Send to payment screen.
    driver.find_element_by_class_name('gl-cta.gl-cta--primary').click()

def autofill_card():
    # Read in card information from file.
    with open('CardInfo.txt','r') as card:
        #Autofill form.
        driver.find_element_by_id('dwfrm_payment_creditCard_number').send_keys(card.readline())
        driver.find_element_by_id('dwfrm_payment_creditCard_cvn').send_keys(card.readline())
        m = (card.readline()).replace('\n','')
        y = (card.readline()).replace('\n','')
        # Open dropdown;
        driver.find_element_by_id('dwfrm_payment_creditCard_month_display_field').click()
        driver.find_element_by_id('dwfrm_payment_creditCard_year_display_field').click()
        list = driver.find_elements_by_class_name('materialize-select-list')
        months = list[0].find_elements_by_css_selector('*')
        # Select month
        for month in months:
            if month.text == m:
                month.click()
        # Select year
        years = list[1].find_elements_by_css_selector('*')
        for year in years:
            if year.text == y:
                year.click()