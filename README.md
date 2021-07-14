## Pura Test Demo

Run tests with the command line command "pytest" in the test directory. Later, other options can be added to the command, introducing parallelization, test reports, etc

## SETUP
Download the chromedriver version for your operating system and matching the version of google chrome installed on your computer (check chrome's "about" page) and place the downloaded file in the test directory. Chromedriver can be downloaded from: https://chromedriver.chromium.org/downloads 

Required modules can be installed from the requirements file by running the command:

```pip install -r requirements.txt```

or individually, by running:

```pip install pytest```
```pip install selenium```

Its generally advised to create a virtual environment first, which causes the packages to be installed only within the context of the virtual environment, but this is not really necessary if you don't use python for other things on your computer.

