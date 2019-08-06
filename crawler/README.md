
# Taylor Pearson Blog Graph     
    
This tool will crawl the [taylorpearson.me](taylorpearson.me) website and build a graph between all pages, so that you could use any graphy-analysis tool of your choice to find most valuable knowledge.  
    
# How to run the crawler    
 ## First install Scrapy 

    $ sudo apt install python3 python3-pip python3-venv  
    
## Install crawler requirements  

    $ git clone https://github.com/vantt/taylorpearsonBlog  
    $ cd taylorpearsonBlog/crawler 
    
    $ python3 -m venv env  
    $ source env/bin/activate  
    $ pip3 install -r requirements.txt  

  
## Run Crawler  
### First run the crawler:  

    $ ./runspider.sh  

  
### Build Graph data  

    $ ./rebuild_graph.py  


## Crawling Result
Result file will be put in [data] folder inside the crawler.
They are in json-line format. Each line is a json-record contains the page-information (title, url) and links to all other pages. 

    {"url": "https://blog.gardeviance.org/2018/10/what-is-expert.html", "id": 3226180912, "title": "What is an expert", "links": {"3226180912": "https://blog.gardeviance.org/2018/10/what-is-expert.html", "3653733001": "https://blog.gardeviance.org/2019/05/a-fond-farewell.html", "1400506942": "https://blog.gardeviance.org/2018/10/rebooting-gds.html", "1844843289": "http://www.wardleymaps.com/tool.html", "2203934499": "http://blog.gardeviance.org/2015/04/the-only-structure-youll-ever-need.html", "2886840601": "http://blog.gardeviance.org/2015/03/wardley-map-set-of-useful-posts.html", "3691906889": "http://blog.gardeviance.org/2013/01/there-must-be-some-way-out-of-here-said.html", "28952583": "https://blog.gardeviance.org/2015/02/an-introduction-to-wardley-value-chain.html", "283084666": "https://blog.gardeviance.org/2013/08/why-would-bezos-buy-washington-post.html", "1432840654": "https://blog.gardeviance.org/2015/08/is-there-trouble-brewing-in-land-of.html", "3466583055": "https://blog.gardeviance.org/2015/03/on-pioneers-settlers-town-planners-and.html", "4264585869": "https://blog.gardeviance.org/2015/06/why-agile-lean-and-six-sigma-must-die.html", "2925317637": "https://blog.gardeviance.org/2012/07/adoption-cycles.html", "385215474": "https://blog.gardeviance.org/2015/11/when-to-use-business-model-canvas-or.html", "73402947": "https://blog.gardeviance.org/2015/08/on-diffusion-and-evolution.html", "886543107": "https://blog.gardeviance.org/2013/11/a-spoiler-for-future-bitcoin.html", "3311135442": "https://blog.gardeviance.org/2014/11/bimodal-it-is-long-hand-for-snafu.html"}}

 
## Graph Analysis
crawling data and final graph data will be put in **[data]** folder
