# Libraries to start up chrome.
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Libraries to find HTML elements.
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait

# Library to insert keys into input fields or otherwise.
from selenium.webdriver.common.keys import Keys

# Libraries to recognize TimeoutException and NoSuchElementException in except clause.
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException

# Library to wait predefined amount.
from time import sleep

# Libraries to change images.
import cv2
import numpy as np

# Library to convert images to bytes.
import io

# Library to send post request to ocr.space.
import requests

# Library to understand results from ocr.space.
import json

# Library to stop code with sys.exit.
import sys

# For moveing image files to another directory.
import os
import shutil

# For only keeping numbers in captcha variable.
import re

# Setup variables.
# white, blue, green, black, red
WORLD = ''
USERNAME = ''
PASSWORD = ''

# ml_kitchen(Köök), ml_cellar(Veinikelder), ml_aerator(Gaseerimismasin)
# ml_distiller(Puskarimasin), ml_cider(Siidriruum), ml_blender(Mahlamasin)
FOODROOM = 'ml_kitchen'
DRINKLEVEL = '1'

# nupuke420_kitchen(Köök), nupuke420_cellar(Veinikelder), nupuke420_aerator(Gaseerimismasin)
# nupuke420_distiller(Puskarimasin), nupuke420_cider(Siidriruum), nupuke420_blender(Mahlamasin)
MIXDRINKSBUTTON = 'nupuke420_kitchen'

# Global variable not meant to be changed for setup.
not_yet_mixing = None

# Sets windows size, goes to crime website and logs in.
def setUpSettingsAndLogIn():
    # Change window size.
    options = Options()
    options.add_argument("--window-size=1500,900")

    # Open crime website.
    global driver
    driver = webdriver.Chrome(options=options)
    driver.get("https://crime.ee/")

    # Expand "punane" world.
    try:
        folder = wait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//span[@id='" + WORLD + "']")))
        folder.click()
        print('Found button for red world')
    except TimeoutException:
        print('Timeout - No button found for red world')

    # Type username
    try:
        inputUserName = wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,"//input[@id='username6']")))
        inputUserName.send_keys(USERNAME)
        print('Found input for username')
    except TimeoutException:
        print('Timeout - No input found for username')

    # Type password
    try:
        inputPassword = wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,"//input[@id='password6']")))
        inputPassword.send_keys(PASSWORD)
        inputPassword.send_keys(Keys.ENTER)
        print('Found input for password')
    except TimeoutException:
        print('Timeout - No input found for password')
        sleep(0.5)

# Enter "Kõrts ja Söökla"
def getToMixingDrinks():
    # Making variable global so the value of the global variable is changed not different local variable is created. 
    global not_yet_mixing
    try:
        tavern = wait(driver, 2).until(EC.visibility_of_element_located((By.XPATH,"//a [@href='?asukoht=tavern']")))
        tavern.click()
        print('Found button for tavern')
        sleep(0.5)
    except TimeoutException:
        print('Timeout - No button found for tavern')
        not_yet_mixing = True
        if foundCaptcha() == True:
            solveCaptcha()

    # Enter food room like "köök"
    try:
        foodRoom = wait(driver, 2).until(EC.visibility_of_element_located((By.XPATH,"//li [@id='" + FOODROOM + "']")))
        foodRoom.click()
        print('Found button for wine cellar')
        sleep(0.5)
    except TimeoutException:
        print('Timeout - No button found for wine cellar')
        not_yet_mixing = True
        if foundCaptcha() == True:
            solveCaptcha()

    # Select drink level
    try:
        levelSelector = wait(driver, 2).until(EC.visibility_of_element_located((By.XPATH,"//option [@value='" + DRINKLEVEL + "']")))
        levelSelector.click()
        print('Found button for level selector')
    except TimeoutException:
        print('Timeout - No button found for level selector')
        not_yet_mixing = True
        if foundCaptcha() == True:
            solveCaptcha()

# Click on mix drink
def mixDrinks():
    # Making variable global so the value of the global variable is changed not different local variable is created. 
    global not_yet_mixing
    not_yet_mixing = False
    i = 1
    while i < 10000:
        try:
            mixDrink = wait(driver, 1).until(EC.visibility_of_element_located((By.XPATH,"//input [@id='" + MIXDRINKSBUTTON + "']")))
            mixDrink.click()
            sleep(0.1)
            i += 1
            print('Found button for mixing drinks ' + str(i))
        except (TimeoutException, ElementNotInteractableException):
            print('Timeout - No button found for mixing drinks')
            if foundCaptcha() == True:
                solveCaptcha()

# Check if captcha appeared
def foundCaptcha():
    try:
        # Check for captcha text.
        wait(driver, 1).until(EC.visibility_of_element_located((By.XPATH,"//button[@class='butn nbt']")))
        print('Found text for captcha')
        return True
    except TimeoutException:
        print('Timeout - No text found for captcha')
        return False

# Download image
def downloadImage():
    with open('filename.png', 'wb') as file:
        try:
            #WineButton = wait(driver, 3).until(EC.visibility_of_element_located((By.XPATH,"//input [@id='nupuke420_cellar']")))
            file.write(driver.find_element("xpath", "//img[@src[contains(.,'etjssd')]]").screenshot_as_png)
            #/html/body/div[2]/div[3]/div[3]/div[1]/table/tbody/tr/td[1]/img For the small screen image popup
            print("Downloaded image")
        except NoSuchElementException:
            print('didt find image file')

#Remove lines from the image
def removeLines():
    # Read the image
    img = cv2.imread("filename.png")

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Get the height and width of the image
    height, width = gray.shape

    # Mark horizontal lines
    for i in range(height):
        if np.all(gray[i, :] == gray[i, 0]):
            img[i, :] = [0, 255, 0] # Mark as green

    # Mark vertical lines
    for j in range(width):
        if np.all(gray[:, j] == gray[:, j][0]):
            img[:, j] = [0, 0, 0] # Mark as black

    # Remove marked lines
    img[(img == [0, 0, 0]).all(axis=2)] = [255, 255, 255] # Replace with white
    img[(img == [0, 255, 0]).all(axis=2)] = [255, 255, 255] # Replace with white

    # Save the modified image
    cv2.imwrite("filenameNoLines.png", img)
    print("Removed lines from captcha iamge")

def removeColor():
    # Remove color from the image
    # Load the image
    img = cv2.imread('filenameNoLines.png')

    # Convert from BGR to HSV color space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define the color range to remove
    lower_bound = (0, 0, 0)
    upper_bound = (195, 195, 195)

    # Create the mask to remove the color
    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    # Create a white image with the same size as the original image
    white_img = np.full(img.shape, 255, dtype=np.uint8)

    # Apply the mask to the white image
    result = cv2.bitwise_and(white_img, white_img, mask=cv2.bitwise_not(mask))

    # Combine the result with the original image using bitwise OR
    result = cv2.bitwise_or(result, img)

    # Save the result
    cv2.imwrite('filenameNoLinesNoColor.png', result)
    print("Removed color from captcha iamge")

def getNumbersFromImage():
    img = cv2.imread("filenameNoLinesNoColor.png")
    height, width, _ = img.shape

    # Cutting image
    # roi = img[0: height, 400: width]
    roi = img

    # Ocr
    url_api = "https://api.ocr.space/parse/image"

    # Compress image. So it's under 1MB.
    _, compressedimage = cv2.imencode(".png", roi, [1, 90])

    # Convert to bytes, because it's needed for sending.
    file_bytes = io.BytesIO(compressedimage)

    result = requests.post(url_api,
                  files = {"filenameNoLinesNoColor.png": file_bytes},
                  data = {"apikey": "K82066701588957",
                          "language": "eng",
                          "OCREngine": 5})

    result = result.content.decode()
    result = json.loads(result)

    parsed_results = result.get("ParsedResults")[0]

    text_detected = parsed_results.get("ParsedText")

    # Only keep numbers in the result.
    text_detected = re.sub(r"[^0-9]", "", text_detected)

    print("Detected numbers from captcha are: " + '"' + text_detected + '"')
    return text_detected

def insertAndSendCaptcha(text_detected):
    # Enter the number into captcha text field
    try:
        inputCaptcha = wait(driver, 1).until(EC.visibility_of_element_located((By.XPATH,"//input[@maxlenght] | //input[@maxlength]")))
        inputCaptcha.send_keys(text_detected)
        print('Found input for captcha text field')
    except TimeoutException:
        print('Timeout - No input found for captcha text field')
        
    # Click on "VASTAMISEKS VAJUTA SIIA" button to solve the captcha.
    try:
        enterCaptchaButton = wait(driver, 1).until(EC.visibility_of_element_located((By.XPATH,"//button[@class='butn lbt'] | //input[@class='butn abt' and not(@name)]")))
        enterCaptchaButton.click()
        print('Clicked on solve captcha button')
    except TimeoutException:
        print('Timeout - didnt find solve captcha button')
        
def saveCaptchaImages():
    # Set the source directory where the files are currently located
    source_dir = ''

    # Set the destination directory where you want to move the files
    destination_dir = 'captcha_images/'

    # Check if the destination directory exists, if not create it
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # Define the mapping between old and new filenames as a dictionary
    filename_mapping = {
        'filename.png': 'filename.png',
        'filenameNoLines.png': 'filenameNoLines.png',
        'filenameNoLinesNoColor.png': 'filenameNoLinesNoColor.png'
    }

    # Move each file to the destination directory with a new filename
    for original_filename in filename_mapping.keys():
        
        # Check if the source file exists
        if os.path.exists(source_dir + original_filename):

            # Get the new filename for the current file
            destination_filename = filename_mapping[original_filename]
            
            # Check if the destination file already exists
            number = 1
            while os.path.exists(os.path.join(destination_dir, destination_filename)):
                extension = os.path.splitext(original_filename)[1]
                destination_filename = filename_mapping.get(original_filename) + '_' + str(number) + extension
                number += 1
            
            # Move the file to the destination directory with the new filename
            shutil.move(source_dir + original_filename, os.path.join(destination_dir, destination_filename))
        else:
            print('File ' + original_filename + ' does not exist in the source directory.')

# Solve the captcha
def solveCaptcha():

    downloadImage()
    removeLines()
    removeColor()

    # Make text_detected equal to the value gotten from getNumbersFromImage function.
    text_detected = getNumbersFromImage()
    
    # If number detection doesn't text number with length of 3 or contains something else than numbers then exit code.
    #if not text_detected.isdigit() and len(text_detected) != 3:
    #    sys.exit("Captcha result is not 3 digits long")

    insertAndSendCaptcha(text_detected)

    #Save captcha images into folders
    saveCaptchaImages()
    
    while foundCaptcha() == True:
        sleep(0.5)

    if (not_yet_mixing == True):
        getToMixingDrinks()

    # Continue making drinks.
    mixDrinks()

# Main function. All the code starts from here.
while True:
    setUpSettingsAndLogIn()
    getToMixingDrinks()

    mixDrinks()
