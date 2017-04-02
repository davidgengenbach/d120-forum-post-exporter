# Export threads from the d120-forum

Just to pass some time :smile:

## Instructions
```shell
pip3 install -r requirements.txt

# This only gets the titles of the threads
./crawler --start-url 'https://www2.fachschaft.informatik.tu-darmstadt.de/forum/viewforum.php?f=219'

# This crawls also the thread posts
./crawler --start-url 'https://www2.fachschaft.informatik.tu-darmstadt.de/forum/viewforum.php?f=219' --crawl-threads
```