from playwright.sync_api import Playwright, sync_playwright, expect
import json
import re
import os
from os import listdir
from os.path import isfile, join
import sys
import webbrowser
import argparse

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root


def test_homepage_has_Playwright_in_title_and_get_started_link_linking_to_the_intro_page(playwright: Playwright, quizDirectory, openbrowser):
    
    #get directory and find excel file. and amount of images
    if not quizDirectory.endswith("\\"):
        quizDirectory += '\\'
    kahootName = [f for f in listdir(quizDirectory) if isfile(join(quizDirectory, f)) and f.endswith(".xlsx") ][0].replace(".xlsx","")
    kahootExcelFile = quizDirectory+[f for f in listdir(quizDirectory) if isfile(join(quizDirectory, f)) and f.endswith(".xlsx") ][0]

    if not quizDirectory.endswith("\\"):
        quizDirectory += '\\'
    images = [f for f in listdir(quizDirectory) if isfile(join(quizDirectory, f)) and f.endswith(".jpg") ]
    questionsAmount = len(images)



    AUTH_PATH = os.path.join(ROOT_DIR, 'auth.json')  # requires `import os`
    #create browser, add authentication token to context
    chromium = playwright.chromium
    browser = chromium.launch(headless=False)
    context = browser.new_context(storage_state=AUTH_PATH)
    page = context.new_page()
    page.goto("https://create.kahoot.it/creator")
    page.screenshot(path="screenshot.png")

    #create quiz & upload of questions. And delete first default question
    visible = page.get_by_role("button", name="Create", exact=True).is_visible()
    if visible:
        page.get_by_role("button", name="Create", exact=True).click()
    page.get_by_role("button", name="Add question").click()
    page.get_by_role("button", name="Import spreadsheet").click()
    with page.expect_file_chooser() as fc_info:
        page.get_by_role("button", name="Select file").click()
    file_chooser = fc_info.value
    file_chooser.set_files(kahootExcelFile)
    page.get_by_role("button", name="Upload", exact=True).click()
    page.get_by_role("button", name="Add questions").click()

    #delete first default question
    page.locator("#kahoot-block-0").get_by_role("button", name="Delete").click()
    page.get_by_role("dialog", name="dialog-confirm-delete-question").get_by_role("button", name="Delete").click()

    #changing of images    
    for i in range(1, questionsAmount+1):
        image = quizDirectory+f"question{i}.jpg"
        page.locator(f'[data-functional-selector="sidebar-block__kahoot-block-{i}"]').click()
        page.get_by_role("button", name="Find and insert media").click()
        with page.expect_file_chooser() as fc_info:
            page.get_by_role("button", name="Upload image").click()
        file_chooser = fc_info.value
        file_chooser.set_files(image)

    #finish
    page.get_by_role("button", name="Save").click()
    page.get_by_placeholder("Enter kahoot title…").fill(kahootName)
    page.get_by_role("button", name="Continue").click()
    # page.get_by_role("button", name="Done").click()

    # with page.expect_popup() as page1_info:
    #     page.get_by_role("button", name="Start Host a live kahoot now").click()
    # page1 = page1_info.value

    pageURL = str(page.url)
    kahootId = pageURL.rpartition('/')[2]
    quizURL = "https://play.kahoot.it/v2/?quizId="+kahootId
    if openbrowser: 
        webbrowser.open_new(quizURL)
    print("Quiz can be found at: " + pageURL)
    print("Quiz can be played at: " + quizURL)


    # ---------------------
    context.close()
    browser.close()

def upload_quiz_to_kahoot(folderPath = "", openbrowser = False):    
    with sync_playwright() as playwright:            
        test_homepage_has_Playwright_in_title_and_get_started_link_linking_to_the_intro_page(playwright, folderPath, openbrowser)

if __name__== "__main__":
    if len(sys.argv) == 2:
        upload_quiz_to_kahoot(sys.argv[1], False)
    else:
        print("No folder inserted")
        
# with sync_playwright() as playwright:
        # test_homepage_has_Playwright_in_title_and_get_started_link_linking_to_the_intro_page(playwright)

