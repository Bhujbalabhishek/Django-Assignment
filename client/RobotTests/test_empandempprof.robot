***Settings***
Library     SeleniumLibrary
Resource    common.robot

*** Test Cases ***
AddEmpandEmpProf
    open browser    ${url}      ${browser}
    login
    sleep   1s
    
    click element   xpath://a[@href="/admin/client/employee/add/"]

    Select From List By index   role    2

    input text  id:id_first_name  abhishek
    input text  id:id_last_name  bhujbal
    input text  id:id_address   Nerul
    input text  id:id_phone   8745961253

    Select From List By index   in_dept    0
    Select From List By index   in_dept    1

    Choose File   css=[type='file']     C:/Users/Abhisekh/Desktop/Django_Projects/Django_Project/cms/media/profile_pics/chai.jpg
    sleep   2s
    click element   xpath://*[@id="employee_form"]/div/div[2]/input[1]
    sleep   2s

    #empprof Link
    click element   xpath://a[@href="/admin/client/empprofile/"] 
    sleep   2s
    TestCheckbox
    DeleteCheckbox

    #employee link
    click element   xpath://a[@href="/admin/client/employee/"]
    TestCheckbox
    DeleteCheckbox

    close browser