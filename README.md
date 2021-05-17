# How to use the tool

1. Clone the repository to your local machine.
 
    ```git clone ```
2. Install all the requirements

    ```pip install -r requirements.txt```
    
3. Install geckodriver

    3.1 Go the [geckodriver page]("https://github.com/mozilla/geckodriver/releases") and download the latest version of the software.
    
    ```wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz```
        
    3.2 Extract the file
    
    ```tar -xvzf geckodriver*```
        
    3.3 Make it executable
    
    ```chmod +x geckodriver```
        
    3.4 Add driver to `/usr/local/bin/`
    
    ```sudo mv geckodriver /usr/local/bin/```
        
4. Configure the storage path in `config.ini` file to store the crawled data.

    ```
    [storage]
    #path=/mnt/mag/google/scholar
    path=/home/kantharaju/google_scholar
    ```

5. Run the tool
    If you want to crawl author publications from file, first add all the author names to the `authors.txt` file and then run the tool.
        
    Tool supports crawling authors and keyword search, to crawl authors run the tool with the argument
     `-authors` followed by `db` or `file` to crawl all the authors from our MAG-Analysis database or from file.
    To crawl publications using keyword, use the argument `--funders` and pass multiple keywords separated by space. 
    The tool developed mainly to crawl publications using the funding reference numbers so the argument is called `funders`.
        
        
    5.1 Running locally

        Fetching authors publications:  
        ```
            python main.py --authors file
        ```

        Fetching authors information:  
        ```
            python main.py --authorsinfo file
        ```
    5.2 Running using Docker
    
        ```
        docker build -t crawler .
        docker run -ti -e type="--authors file" crawler
        docker run -ti -e type="--authorsinfo file" crawler 
        or 
        docker run -ti -e type="--authors db" crawler 
        or
        docker run -ti -e type="--funder keyword1 keyword2" crawler 
        ```
    
   
6. Authors crawled data is stored in the configured path, for each author there will be new file stored.

    
