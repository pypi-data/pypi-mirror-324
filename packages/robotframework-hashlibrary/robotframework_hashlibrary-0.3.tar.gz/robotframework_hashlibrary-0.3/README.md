
# HashLibrary for Robot Framework®

HashLibrary is an  library for Robot Framework.  
It generates hashes based on the given inputs.

---
## Installation
If you already have Python >= 3.8 with pip installed, you can simply run:  
`pip install robotframework-hashlibrary`

---
## Getting started
Some examples how to import and use the library.

``` robotframework
*** Settings ***
Library            HashLibrary

*** Variables ***
${TEST_STRING}    david

*** Test Cases ***
Generate hash for string
    ${hash}    Get Base64 Hash From String  ${TEST_STRING}

```

