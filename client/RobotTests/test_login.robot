***Settings***
Library     SeleniumLibrary
Resource    common.robot


*** Test Cases ***
LoginTest
    open browser    ${url}     ${browser}
    login
    close browser

InvalidLoginTest
    open browser    ${url}     ${browser}
    input text  id:id_username  test  
    sleep   1s
    input text  id:id_password  Abhishek
    sleep   1s
    Logindata  
    sleep   1s 
    close browser
