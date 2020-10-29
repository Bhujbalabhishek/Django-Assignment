*** Variables ***

${browser}  chrome
${url}  http://localhost:8000/admin/login/?next=/admin/



*** Keywords ***
login
    input text  id:id_username  admin  
    sleep   1s
    input text  id:id_password  Abhishek123
    sleep   1s
    Logindata   

Logindata
    click element   xpath://*[@id="login-form"]/div[3]/input

#Checkboxes
TestCheckbox
    Select checkbox     xpath://*[@id="result_list"]/tbody/tr[1]/td/input

DeleteCheckbox
    Select From List By Value   action  delete_selected
    #click on to GO button
    click element   xpath://*[@id="changelist-form"]/div[1]/button
    #are you sure?
    click element   xpath://*[@id="content"]/form/div/input[4]
    sleep   1s