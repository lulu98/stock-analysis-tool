# Investing Calculator

## Introduction

When investing in the stock market, most people put their money into a company
based on news headlines and gut feelings. In order to gain more confidence in
your investments, it is recommended to put a potential company through a
thorough financial background check and analyse the financial health of the
company. This requires going through financial statements of the company and
gather as much data as possible. The more data you have collected, the more
confident you can be in your investment. Nowadays, this data can be pulled from
websites and public APIs on the internet; manually collecting this data can
still be tiresome. So why not let a program calculate all the necessary numbers
and ratios and put it cleanly in a PDF document all in one place?

This system provides a procedural way to get financial data for a
publicly-traded company from a web API and create a financial analysis based on
the fundamental data. This process is integrated into a pipeline to automate the
process. At the end of it, a PDF document with the financial analysis is
produced. This is my own personal investment strategy based on several sources,
listed below. The process can be adapted to anyone's personal investing strategy
and should provide a good starting point to construct your own streamlined
process.

## Origin of the idea

Recently I got interested in the idea of investing your money in order to get a
return in the long term. Since I am really not interested in all the fuzz and
following the news 24/7, I mostly read up on the traditional ways of investing
as the likes of Warren Buffett, Charlie Munger, Mohnish Pabrai, Peter Lynch and
Phil Town; I read some books and did my research. What striked me was that with
enough information, you can gain confidence in your investment decisions, simply
based on information of the past. So, I started to learn how to read financial
statements and build my own investment strategy, mostly based on the aforementioned
people. The problem is I find reading these statements incredibly tiresome; for
my strategy to work, I have to gather a lot of data and make a lot of calculations
though. But I don't really want to spend too much time on going through financial
statements. Luckily for me, there are websites that offer to get this data, but
this still does not relieve me of checking all these numbers and doing most
calculations by hand. The solution in the end is to pull the required data from
a Web API and construct the ratios and calculations locally via a script and put
this data inside a document. As a result, I have all the required data in one
place and don't waste my time on first finding and noting down all this data.
This saves a ton of time!

## Prerequisites

Latex must be installed:

- `miktex`

The following Python packages are required:

- `json2latex`

Other packages include:

- `mdl`
- `jsonlint-php`
- `lacheck`
- `chktex`

## Project Structure

This project has the following structure:

```bash
|__ README.md
|__ CHANGELOG.md
|__ src
    |__ docs: sphinx documentation for Python scripts
    |
    |__ main: source code
    |   |__ code: Python scripts
    |   |__ config: configuration files
    |   |__ resources: template + data files
    |
    |__ test: test code
        |__ linter: linter scripts
        |__ unit_test: unit test scripts
        |__ ...

```

## System Architecture

![Architecture Diagram](./images/workflow.png)

## Description

In the flowchart you can see the analysis pipeline. It consists of two stages:
the first stage pulls the financial data form the Web API, the second stage does
a financial analysis and creates a PDF. At the end of the pipeline, a PDF is
generated with the corresponding financial data included. Additional custom text
additions can be included.

## Web API: EOD Historical Data

I chose `EOD Historical Data`[1] as the Web API for this project. It provides
fundamental data over the last 30 years for most publicly-traded companies. At
the time of writing the subscription model has several tiers; the "Fundamentals
Data Feed" can be purchased for 50 euros and lets you use the Search API as well
as the Fundamentals API. This gives you access to fundamental data of publicly
traded companies over the last 30 years. There is no need to also gain access to
Real-Time data for this project.

Since I really don't intend to spend too much money on data that will only change
once a year, the project can be used by subscribing to the Web API for one month.
During this month, it is possible to pull all the data of the required stocks. I
store the data as JSON files in the `data` folder.

In order to make use of this project, you have to subscribe to the API once. I
am sorry, but I will not provide any data here. If you want to get a feel for
how this project works, you can create a report for the company `Apple Inc.` since
EOD provides the data for this company for free.

## Stage 1: Getting financial data and store it locally

After subscribing to the API, you can trigger stage 1 of the pipeline in order
to get fundamental data for a company. This stage can be triggered by the
`stage01.py` script in one of the following ways:

- Pull data for one specific company:

```bash
./stage01.py -k <api_key> -i <isin>
```

- Pull data for all stocks listed in `stocks.json`:

```bash
./stage01.py -k <api_key>
```

Either command will pull the requested data as a JSON file into `src/data`. You
can back up this data into a cloud of your choice.

That is basically the dependence on the Web API. As soon as you have the data
locally, the reports can be build offline.

## Stage 2: PDF generation

Stage 2 operates on the locally accessible data in `src/data`. Based on a specific
company's data, the `stage02.py` script creates a latex document structure and
creates custom JSON files `fund_data.json` and `calc_data.json`. The JSON files
initially have placeholders that are replaced with extracted data from the company
JSON files. These custom JSON files form the backend, so in case the API changes,
it is quite straight forward to adapt the project. Stage 2 can be triggered as
follows:

```bash
./stage02.py -i <isin>
```

This stage uses the `json2latex`[2] python package in order to make it possible
to access data from the Latex file similar to a database access. Using a database
in Latex is not as straight-forward as I wished for, so the `json2latex` package
seems like a good alternative. According to sources like StackOverflow, it is
possible to use an SQL database with Luatex, but with my MikTex setup, it does
not compile.

## Stage 3: Manual Edit

After stage 2, we have all the financial data and analysis completed and the
placeholders of the Latex template have been replaced by the corresponding real
data. As part of the analysis, the user has the option to manually edit the
corresponding Latex template. It is possible to manually trigger a PDF build with
the following command in the corresponding folder:

```bash
make pdf
```

This creates a `main.pdf` file in the `build` subfolder.

## Documentation

For this project, I decided to use Sphinx for the code documentation. According
to the Internet, it seemed to be the preferred option for Python code compared
to for example Doxygen.

The documentation for this project is located in the `./docs` directory and
uses the `sphinx_rtd_theme` that can be installed via `pip`. When first building
the project, the following command must be executed:

```bash
sphinx-quickstart
```

The documentation can be build with the following command when located in `docs`:

```bash
sphinx-apidoc -o ./source ../src
```

And the HTML documentation can then be created via:

```bash
make html
```

If the documentation is required as a PDF, execute the following command:

```bash
make latexpdf
```

PDF creation requires `latexmk` to be installed.

## Linters

In order to comply with proper formatting guidelines, the project uses different
linters.

### Markdown linter

The linter for Markdown files is:

- `mdl`

### JSON linter

The linter for JSON files is:

- `jsonlint-php`

### Latex linter

The linters for Latex files is:

- `chktex`
- `lacheck`

## TODO

- Rename project to `stock analysis tool`.
- Unit test python functions
- linters for project files
- Create a CI/CD workflow.

## Sources

[1] [EOD](https://eodhistoricaldata.com/)

[2] [JSON2Latex](https://pypi.org/project/json2latex/)
