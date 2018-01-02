*** Settings ***
Library           AppiumLibrary
Library           DatabaseLibrary
Library           Collections

*** Variables ***
${REMOTE_URL}           http://localhost:4723/wd/hub
${PLATFORM_NAME}        Android
${PLATFORM_VERSION}     6.0
${DEVICE_NAME}          872c0992
${APP}                  ${CURDIR}/android_apps/Sepulsa_4.0.0-sandbox.apk
${PACKAGE}              com.sepulsa.androiddev
${DBHost}               localhost
${DBName}               pavoGUI
${DBPass}               4izatgantenG
${DBPort}               3306
${DBUser}               root
${count}                0
${tempImageDir}         app/practitest/tempImage

*** Keywords ***
Connect Database
    Connect To Database    pymysql    ${DBName}    ${DBUser}    ${DBPass}    ${DBHost}    ${DBPort}

Disconnect Database
    Disconnect From Database
    Close Application

Buka Aplikasi sepulsa, kemudian tunggu tulisan "${text}" muncul
    Open Application        ${REMOTE_URL}       platformName=${PLATFORM_NAME}      platformVersion=${PLATFORM_VERSION}          deviceName=${DEVICE_NAME}       app=${APP}          automationName=appium       appPackage=${PACKAGE}
    Wait Until Page Contains        ${text}       15s
    ${count}=                   Evaluate            ${count}+1
    Set suite variable          ${count}             ${count}
    Capture Page Screenshot         ${tempImageDir}/${count}_initial_page.png

Buka Aplikasi sepulsa, kemudian tunggu tulisan "${text}" muncul tanpa Screenshot
    Open Application        ${REMOTE_URL}       platformName=${PLATFORM_NAME}      platformVersion=${PLATFORM_VERSION}          deviceName=${DEVICE_NAME}       app=${APP}          automationName=appium       appPackage=${PACKAGE}
    Wait Until Page Contains        ${text}       15s

Tekan tombol "${tombol}" di Aplikasi, kemudian tunggu tulisan "${text}"
    @{queryResults} =    Query    SELECT type, value FROM element_web WHERE name = '${tombol}';
    Log Many                            @{queryResults}
    Log                                 ${queryResults[0][1]}, ${queryResults[0][0]}
    Wait Until Element Is Visible       ${queryResults[0][0]}=${queryResults[0][1]}        15s
    Click Element                       ${queryResults[0][0]}=${queryResults[0][1]}
    Wait Until Page Contains            ${text}             15s
    ${count}=                           Evaluate            ${count}+1
    Set suite variable                  ${count}            ${count}
    Capture Page Screenshot             ${tempImageDir}/${count}_push_button_${tombol}.png

Tekan tombol "${tombol}" di Aplikasi, kemudian tunggu tulisan "${text}" tanpa Screenshot
    @{queryResults} =    Query    SELECT type, value FROM element_web WHERE name = '${tombol}';
    Log Many                            @{queryResults}
    Log                                 ${queryResults[0][1]}, ${queryResults[0][0]}
    Wait Until Element Is Visible       ${queryResults[0][0]}=${queryResults[0][1]}        15s
    Click Element                       ${queryResults[0][0]}=${queryResults[0][1]}
    Wait Until Page Contains            ${text}             15s

Input ke "${field_text}" di Aplikasi, kemudian isi dengan "${value}"
    @{queryResults} =    Query    SELECT type, value FROM element_web WHERE name = '${field_text}';
    Log Many    @{queryResults}
    Log         ${queryResults[0][1]}, ${queryResults[0][0]}
    Input Text      ${queryResults[0][0]}=${queryResults[0][1]}       ${value}
    ${count}=                   Evaluate            ${count}+1
    Set suite variable          ${count}             ${count}
    Capture Page Screenshot     ${tempImageDir}/${count}_insert_text_${value}.png

Input ke "${field_text}" di Aplikasi, kemudian isi dengan "${value}" tanpa Screenshot
    @{queryResults} =    Query    SELECT type, value FROM element_web WHERE name = '${field_text}';
    Log Many    @{queryResults}
    Log         ${queryResults[0][1]}, ${queryResults[0][0]}
    Input Text      ${queryResults[0][0]}=${queryResults[0][1]}       ${value}

Cari tombol "${tombol}" di bawah
    @{queryResults} =    Query    SELECT type, value FROM element_web WHERE name = '${tombol}';
    Log Many                            @{queryResults}
    Log                                 ${queryResults[0][1]}, ${queryResults[0][0]}
    ${iteration}    Set Variable        0
    : FOR             ${iteration}        IN RANGE        0       10
    \    Swipe           30          600         30          100
    \    ${find}    Run Keyword And Return Status    Wait Until Page Contains Element    ${queryResults[0][0]}=${queryResults[0][1]}
    \    Log        ${find}
    \    Run Keyword If    ${find}     Exit For Loop
    \    ${iteration}    Set Variable    ${iteration}+1
    ${count}=                           Evaluate            ${count}+1
    Set suite variable                  ${count}            ${count}
    Capture Page Screenshot             ${tempImageDir}/${count}_scroll_down_to_${tombol}.png


Valid Login Android
    Given Buka Aplikasi sepulsa, kemudian tunggu tulisan "Mudah Cepat dan Aman" muncul tanpa Screenshot
    And Tekan tombol "Button Skip Android" di Aplikasi, kemudian tunggu tulisan "SIGN IN" tanpa Screenshot
    When Input ke "Field Username Android" di Aplikasi, kemudian isi dengan "aizat@sepulsa.com" tanpa Screenshot
    And Input ke "Field Password Android" di Aplikasi, kemudian isi dengan "4izatgantenG" tanpa Screenshot
    And Tekan tombol "Button Show Password Android" di Aplikasi, kemudian tunggu tulisan "4izatgantenG" tanpa Screenshot
    Then Tekan tombol "Button Sign In Android" di Aplikasi, kemudian tunggu tulisan "Sepulsa Kredit"