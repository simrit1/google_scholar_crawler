[![License: Unlicense](https://img.shields.io/badge/license-Unlicense-blue.svg)](http://unlicense.org/)

# Motivation:
Many research insitutes and research driven companies are required to obtain information about author details (papers information, interests) or even find out who are top publishing or cited authors. For all of this information and some extra analysis one will have to extract information for them. Keeping such a motivation in mind we have introduced a CLI tool to crawl for information and obtain the results accordingly.

## The tool is built over:
[Scholarly](https://scholarly.readthedocs.io/en/latest/?badge=latest)

# Using the tool

## Clone the repository to your local machine.
 
   ```git clone https://github.com/bethgelab/google_scholar_crawler.git```
## Install all the requirements

   ```pip install -r requirements.txt```
    
## Install geckodriver

   3.1 Go the [geckodriver page]("https://github.com/mozilla/geckodriver/releases") and download the latest version of the software.
    
   ```wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz```
        
   3.2 Extract the file
    
   ```tar -xvzf geckodriver*```
        
   3.3 Make it executable
    
   ```chmod +x geckodriver```
        
   3.4 Add driver to `/usr/local/bin/`
    
   ```sudo mv geckodriver /usr/local/bin/```

   3.5 Setup tor: Some might need sudo permissions
    
   ```sudo ./setup_tor.sh```
        
## Configure the storage path in `config.ini` file to store the crawled data.

   ```
    [storage]
    path=/home/user/your_saveable_folder
   ```

## Run the tool
          
    Tool supports crawling for authors, authors profile, keyword based authors and publications, you can crawl authors in two ways using names and google scholar id's. Publications can be crawled using keywords, we mainly support funding reference numbers search and other option using author names.

## Examples:
<TODO: Check if the examples are correct below>

### Fetching publications using funding reference numbers

   ```
        python main.py --funders fundingnumber1 fundingnumber2
   ```

### Fetching information about authors via keyword:  
   ```
      # Setup the n_hits in config.ini to your suitable value. (Default is 20)
      # Example keyword: machine_learning berlin
         python main.py --keyword --input-file path/to/input/file.txt
   ```
### Fetching authors publications:  
   ```
        python main.py --authors-publications --input-file path/to/input/file.txt
   ```
### Fetching authors information from names:  
   ```
        python main.py --authors-by-name --input-file path/to/input/file.txt
   ```
### Fetching authors information from Google Scholar id's:  
   ```
         python main.py --authors-by-id --input-file path/to/input/file.txt
   ```
### Fetching authors information through keyword:  
   ```
         python main.py --authors-by-keyword --input-file path/to/input/file.txt
   ```

5.2 Running using Docker

   ```
    docker build -t crawler .
    docker run -ti -e type="--authors_publications --input-file path/to/input/file.txt" crawler
    or
    docker run -ti -e type="--authors-by-name --input-file path/to/input/file.txt" crawler
    or 
    docker run -ti -e type="--authors-by-name --input-file path/to/input/file.txt" crawler 
    or
    docker run -ti -e type="--funder keyword1 keyword2" crawler 
   ```
    
   
6. Authors crawled data is stored in the configured path, for each author there will be new file stored.

## Plans for the next releases:
- [ ] Creation of visualization module
- [ ] Creation of reporting module with multiple reporting supports
- [ ] Adding multiple backends for crawling apart from google scholar

## Maintainers
* Kantharaju CN, github: [kantharajucn](https://github.com/kantharajucn)
* Subash Prakash, github: [prakass1](https://github.com/prakass1)

## © Copyright
See [LICENSE](LICENSE) for details.