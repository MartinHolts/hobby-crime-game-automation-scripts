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

# Setup variables.
WORLD = 'red'
USERNAME = 'ToiletFace9000'
PASSWORD = 'midagiuut'

# ml_kitchen(Köök), ml_cellar(Veinikelder), ml_aerator(Gaseerimismasin), ml_distiller(Puskarimasin), ml_cider(Siidriruum), ml_blender(Mahlamasin)
FOODROOM = 'ml_kitchen'
DRINKLEVEL = '53'

# nupuke420_kitchen(Köök), nupuke420_cellar(Veinikelder), nupuke420_aerator(Gaseerimismasin)
# nupuke420_distiller(Puskarimasin), nupuke420_cider(Siidriruum), nupuke420_blender(Mahlamasin)
MIXDRINKSBUTTON = 'nupuke420_kitchen'

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
    try:
        tavern = wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,"//a [@href='?asukoht=tavern']")))
        tavern.click()
        print('Found button for tavern')
        sleep(0.5)
    except TimeoutException:
        print('Timeout - No button found for tavern')

    # Enter food room like "köök"
    try:
        foodRoom = wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,"//li [@id='" + FOODROOM + "']")))
        foodRoom.click()
        print('Found button for wine cellar')
        sleep(0.5)
    except TimeoutException:
        print('Timeout - No button found for wine cellar')

    # Select drink level
    try:
        levelSelector = wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,"//option [@value='" + DRINKLEVEL + "']")))
        levelSelector.click()
        print('Found button for level selector')
    except TimeoutException:
        print('Timeout - No button found for level selector')

# Click on mix drink
def mixDrinks():
    i = 1
    while i < 10000:
        try:
            mixDrink = wait(driver, 3).until(EC.visibility_of_element_located((By.XPATH,"//input [@id='" + MIXDRINKSBUTTON + "']")))
            mixDrink.click()
            sleep(0.1)
            i += 1
            print('Found button for mixing drinks ' + str(i))
        except TimeoutException:
            print('Timeout - No button found for mixing drinks')
            solveCaptcha()

# Check if captcha appeared
def checkForCaptcha():
    try:
        # Check for captcha text.
        wait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[2]/div[3]/div[3]/div[1]/div/div/p")))
        print('Found text for captcha')
        global foundCaptcha
        foundCaptcha == True
    except TimeoutException:
        print('Timeout - No text found for captcha')

# Solve the captcha
def solveCaptcha():
    # Download image
    with open('filename.png', 'wb') as file:
        try:
            #WineButton = wait(driver, 3).until(EC.visibility_of_element_located((By.XPATH,"//input [@id='nupuke420_cellar']")))
            file.write(driver.find_element("xpath", '/html/body/div[2]/div[3]/div[3]/div[1]/table/tbody/tr/td[1]/img').screenshot_as_png)
            #/html/body/div[2]/div[3]/div[3]/div[1]/table/tbody/tr/td[1]/img For the small screen image popup
            print("Downloaded image")
        except NoSuchElementException:
            print('didt find image file')

    #Remove lines from the image
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
    print(text_detected)

    # If number detection doesn't text number with length of 3 or contains something else than numbers then exit code.
    if not text_detected.isdigit() and len(text_detected) != 3:
        sys.exit("Captcha result is not 3 digits long")
    
    # Enter the number into captcha text field
    try:
        inputUserName = wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,"/html/body/div[2]/div[3]/div[3]/div[1]/table/tbody/tr/td[2]/p/input[1]")))
        inputUserName.send_keys(text_detected)
        print('Found input for captcha text field')
    except TimeoutException:
        print('Timeout - No input found for captcha text field')
        
    # Click on "VASTAMISEKS VAJUTA SIIA" button to solve the captcha.
    try:
        inputUserName = wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,"/html/body/div/div[2]/table/tbody/tr/td/table/tbody/tr[3]/td/form[2]/input[2]")))
        inputUserName.click()
        print('Clicked on solve captcha button')
    except TimeoutException:
        print('Timeout - didnt find solve captcha button')

    # Check for captcha button again to see if it solved captcha.
    try:
        inputUserName = wait(driver, 3).until(EC.visibility_of_element_located((By.XPATH,"/html/body/div/div[2]/table/tbody/tr/td/table/tbody/tr[3]/td/form[2]/input[2]")))
        sys.exit("Captcha solving failed")
    except TimeoutException:
        print('Timeout - Solved captcha sucessfully')

    
    # Continue making drinks.
    mixDrinks()

# Main function. All the code starts from here and is the only one that calls other functions.
def main():
    setUpSettingsAndLogIn()
    getToMixingDrinks()

    mixDrinks()

main()