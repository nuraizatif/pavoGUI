*** Settings ***
Library         Selenium2Library
Library         DatabaseLibrary
Library         Collections

*** Variables ***
${DBHost}         localhost
${DBName}         pavoGUI
${DBPass}         4izatgantenG
${DBPort}         3306
${DBUser}         root
${count}          0
${tempImageDir}         app/practitest/tempImage

*** Keywords ***
Connect Database
    Connect To Database    pymysql    ${DBName}    ${DBUser}    ${DBPass}    ${DBHost}    ${DBPort}

Disconnect Database
    Disconnect From Database
    Close all browsers

Buka browser "${browser}" dan menuju halaman "${url}", kemudian tunggu tulisan "${text}" muncul
    Open Browser                ${url}      ${browser}
    Wait Until Page Contains    ${text}
    ${count}=                   Evaluate            ${count}+1
    Set suite variable          ${count}             ${count}
    Capture Page Screenshot     ${tempImageDir}/${count}_homepage.png

Buka browser "${browser}" dan menuju halaman "${url}", kemudian tunggu tulisan "${text}" muncul tanpa Screenshot
    Open Browser                ${url}      ${browser}
    Wait Until Page Contains    ${text}

Tekan tombol "${tombol}", kemudian tunggu tulisan "${text}"
    @{queryResults} =    Query    SELECT type, value FROM element_web WHERE name = '${tombol}';
    Log Many    @{queryResults}
    Log         ${queryResults[0][1]}, ${queryResults[0][0]}
    Wait Until Element Is Visible       ${queryResults[0][0]}=${queryResults[0][1]}        15s
    Wait Until Element Is Enabled       ${queryResults[0][0]}=${queryResults[0][1]}        15s
    Click Element               ${queryResults[0][0]}=${queryResults[0][1]}
    Wait Until Page Contains    ${text}            15s
    ${count}=                   Evaluate            ${count}+1
    Set suite variable          ${count}             ${count}
    Capture Page Screenshot     ${tempImageDir}/${count}_push_button_${tombol}.png

Tekan tombol "${tombol}", kemudian tunggu tulisan "${text}" tanpa Screenshot
    @{queryResults} =    Query    SELECT type, value FROM element_web WHERE name = '${tombol}';
    Log Many    @{queryResults}
    Log         ${queryResults[0][1]}, ${queryResults[0][0]}
    Wait Until Element Is Visible       ${queryResults[0][0]}=${queryResults[0][1]}        15s
    Wait Until Element Is Enabled       ${queryResults[0][0]}=${queryResults[0][1]}        15s
    Click Element               ${queryResults[0][0]}=${queryResults[0][1]}
    Wait Until Page Contains    ${text}            15s

Input ke "${field_text}", kemudian isi dengan "${value}"
    @{queryResults} =    Query    SELECT type, value FROM element_web WHERE name = '${field_text}';
    Log Many    @{queryResults}
    Log         ${queryResults[0][1]}, ${queryResults[0][0]}
    Input Text      ${queryResults[0][0]}=${queryResults[0][1]}       ${value}
    ${count}=                   Evaluate            ${count}+1
    Set suite variable          ${count}             ${count}
    Capture Page Screenshot     ${tempImageDir}/${count}_insert_text_${value}.png

Input ke "${field_text}", kemudian isi dengan "${value}" tanpa Screenshot
    @{queryResults} =    Query    SELECT type, value FROM element_web WHERE name = '${field_text}';
    Log Many    @{queryResults}
    Log         ${queryResults[0][1]}, ${queryResults[0][0]}
    Input Text      ${queryResults[0][0]}=${queryResults[0][1]}       ${value}

Valid Login
    Given Buka browser "Chrome" dan menuju halaman "https://p.sepulsa.id", kemudian tunggu tulisan "Jual Isi Pulsa Online Murah" muncul tanpa Screenshot
    When Tekan tombol "Login Button", kemudian tunggu tulisan "Masuk Akun Sepulsa" tanpa Screenshot
    And Input ke "Field Username", kemudian isi dengan "aizat@sepulsa.com" tanpa Screenshot
    And Input ke "Field Password", kemudian isi dengan "4izatgantenG" tanpa Screenshot
    Then Tekan tombol "Masuk Button", kemudian tunggu tulisan "Sepulsa Kredit"