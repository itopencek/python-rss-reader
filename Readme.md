# RSS Parser - Semestral work

This is a project I made for a course BI-PYT. Specification about the topic of this project is in file `havasiva.pdf`.

## Dependencies

These are the dependencies, which are needed to run this project (with their used version):

```
Flask==2.0.2
Flask_SQLAlchemy==2.5.1
MarkupSafe==2.0.1
numpy==1.21.4
pandas==1.3.4
pytest==4.6.9
```

To easily install these dependencies, you can run:

```
pip install -r requirements.txt
```
Thanks to [stackoverflow](https://stackoverflow.com/a/53925733).

## How to start

After you've downloaded the dependencies, run `main.py` to start this web app.

```
semestral_work> python3 main.py
```

Then go to

```
http://localhost:5000
```

### About project

This web app should have simple interface (website). On the main page, you can see parsed articles (up to 7 pages of them).
You also have pages to show/delete sites (from which the articles can be parsed) and add new site. There is an additional webpage showing simple statistics.

Database is also filled with different sites (in czech, slovak and english) and their respective articles - just to showcase everything.

Hopefully, everything is understandable from the code itself. Everything should also be explained in comments. If there are any problems feel free to contact me.

## How to run tests

Go to `ArticleParserApp/test` and run pytest.

```
semestral_work/ArticleParserApp/test> pytest-3
```


by Ivan Havasi