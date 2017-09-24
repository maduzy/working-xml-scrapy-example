# Working XML Scrapy example
I'm aiming to provide a functioning example to get started in Scrapy and outputting the results to an XML file. This example has everything setup to scrape information from a website and storing it into an XML structure.

# Installing Scrapy
This project assumes you have Scrapy installed on your system. Please refer do Scrapy's documentation [here](https://doc.scrapy.org/en/latest/ "Scrapy's documentation website")

The easiest way to install Scrapy is to use **pip** which you can get [here](https://pip.pypa.io/en/stable/installing/ "pip's website").
Then you can run the command from your CLI:
```
# pip install scrapy
```

If you can't install Scrapy, you're probably missing a few packages. Usually you can easily solve this with the following command that should gather everything you need:
```
# yum install gcc libffi-devel python-devel openssl-devel
```

If you're unable to run Scrapy due to a Twisted error, make sure you have openssl upgraded. You can work around it by downgrading Twisted:
```
# pip install Twisted==16.0.0
```

Also make sure you have PIL installed:
```
# pip install Pillow
```

Finally, make sure you're inside the project's directory and you should be able to run the spider with:
```
# scrapy crawl bookspider
```
