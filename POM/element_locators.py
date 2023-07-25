""" This File contains web element locators for all pages. """


class CommonLocators:
    pass


class home_page:
    search_box = {
        "locator_type": "xpath",
        "locator_value": "//*[@id='APjFqb']",
    }
    search_buttom = {
        "locator_type": "xpath",
        "locator_value": "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[4]/center/input[1]",
    }
    outer_page = {
        "locator_type": "xpath",
        "locator_value": "/html/body/div[1]/div[3]/form/div[1]",
    }
