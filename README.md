# How to use the tool

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
        
## Configure the storage path in `config.ini` file to store the crawled data.

   ```
    [storage]
    #path=/mnt/mag/google/scholar
    path=/home/kantharaju/google_scholar
   ```

## Run the tool
          
    Tool supports crawling authors and publications, you can crawl authors in two ways using names and google scholar id's. Publications can be crawled using keywords, we mainly support funding reference numbers search and other option using author names.
    If you want to crawl authors or publications from file, first add all the author names to the file and then run the tool by passing the file name to the argument `input-file``.
        
        
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

    
