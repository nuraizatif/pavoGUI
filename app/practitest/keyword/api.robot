*** Keywords ***
Buat Sesi dengan nama "${nama}" dan url "${url}"
    Create Session              ${nama}                     ${url}
Request "${nama}" ke path "${path}"
    ${resp_temp}=               Get Request                 ${nama}                 ${path}
    Set suite variable          ${resp}             ${resp_temp}
Http request codenya harus "${http_response}"
    Should Be Equal As Strings          ${resp.status_code}         ${http_response}
Di dalemnya harus ada nilai "${nilai}"
    Dictionary Should Contain Value     ${resp.json()}              ${nilai}