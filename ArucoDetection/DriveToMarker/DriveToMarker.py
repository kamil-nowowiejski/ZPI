
def driveToMarker(rvec, tvec, driver):
    driver.skrec(-rvec[1])
    driver.jedzProsto(-tvec[0])
    driver.skrec(3.14/2)