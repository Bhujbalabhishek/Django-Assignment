***Settings***
Library     SeleniumLibrary
Resource    common.robot

*** Test Cases ***
AddCompany 
    open browser    ${url}      ${browser}
    login

    sleep   1s
    # Set Focus To Element  
    click element   xpath://a[@href="/admin/client/company/add/"]

    input text  id:id_company_name  Demo
    sleep   1s
    input text  id:id_department_set-0-dept_name    HR
    sleep   1s

    click element   xpath://*[@id="company_form"]/div/div[2]/input[1]
    sleep   1s
    TestCheckbox
    DeleteCheckbox

    close browser
    