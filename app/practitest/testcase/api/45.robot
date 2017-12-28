*** Settings ***
Library     Collections
Library     RequestsLibrary
Resource     ../../keyword/api.robot

*** Test Cases ***
Test
     Given Buat Sesi dengan nama "local" dan url "http://localhost:8000"
     When Request "local" ke path "/api/v1/hello"
     Then Http request codenya harus "200"
     and Di dalemnya harus ada nilai "HelloWorld"


