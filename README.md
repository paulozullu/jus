# Jusbrasil - Desafio Backend Engineer | Data

## Description
This Django project contains a scrapy project that receives parameters entered by the user in a web page, then collects data from a weppage, saves this data in the database and returns it to the user in a result page.

## Installation
To install this project, plese follow steps below:

1. Install virtualenv
    ```
    sudo pip install virtualenv
    ```
    
2. Clone this project
    ```
    git clone https://github.com/paulozullu/jus.git
    ```
    
3. Inside the created folder (**jus**), run the command below to create the virtual environment
    ```
    virtualenv envname
    ```
    
4. Activate the new virtual environment
    ```
    virtualenv envname/bin/activate
    ```
    
5. Install dependencies
   ```
   pip install -r requirements.txt
   ```
 
 6. Edit the lib scrapyrt to allow send parameters to the spider via POST requests. [Issue link](https://github.com/scrapinghub/scrapyrt/issues/29)
 - Access your scrapyrt installation  folder:
 ```
 $ cd envname/lib/python2.7/site-packages/scrapyrt/
 ```
 - Open the file ```resources.py``` and add the lines below before ```dfd = self.run_crawl```:
 ```
crawler_params = api_params.copy()
for api_param in ['max_requests', 'start_requests', 'spider_name', 'url']:
    crawler_params.pop(api_param, None)
kwargs.update(crawler_params)
 ```   
 
 7. Run! (:
- Access the project root folder and run:
```
$ python manage.py runserver
```
- Access the folder jus_crawler inside the root folder and run:
```
$ scrapyrt
```
- Go to you preferred web browser and point to [localhost](http://localhost:8000)

## Work Environment

### PC Specs (Asus K46CA):
- Processor: Intel Core I7-3517U 
- RAM: 8Gb
- SSD: 24Gb
- HD: 1Tb

### SO:
- KDE Neon User Edition 5.13 (16.04 LTS)
- Plasma 5.13.4

### Development IDE:
- PyCharm 2018.2.2 (Community Edition)
- Build #PC-182.4129.34, built on August 21, 2018
- JRE: 1.8.0_152-release-1248-b8 amd64
- JVM: OpenJDK 64-Bit Server VM by JetBrains s.r.o
- Linux 4.15.0-33-generic
