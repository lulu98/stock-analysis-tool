# Stock Analysis Tool

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

## Prerequisites

Latex must be installed:

- `miktex`

The following packages are required:

- `json2latex`
- `mdl`
- `jsonlint-php`
- `lacheck`
- `chktex`
- `coverage`
- `pytest`
- `coverage`
- `pycodestyle`
- `pylint`
- `pyflakes`
- `mccabe`

## Project Structure

This project has the following structure:

```bash
|__ README.md
|__ CHANGELOG.md
|__ demo
|   |__ demo.pdf: examplery PDF output for Apple Inc stock
|   |__ handbook.pdf: handbook PDF that explains ratios used in the stock analysis
|
|__ src
    |__ docs: sphinx documentation for Python scripts
    |
    |__ main: source code
    |   |__ code: Python scripts
    |   |__ config: configuration files
    |   |__ resources:
    |       |__ template: Latex template
    |       |__ data: fundamental financial data stored as JSON files
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
store the data as JSON files in the `src/main/resources/data` folder.

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

- Pull data for all stocks listed in `src/main/config/stocks.json`:

```bash
./stage01.py -k <api_key>
```

Either command will pull the requested data as a JSON file into
`src/main/resources/data`. You can back up this data into a cloud of your
choice.

That is basically the dependence on the Web API. As soon as you have the data
locally, the reports can be build offline.

## Stage 2: PDF generation

Stage 2 operates on the locally accessible data in `src/main/resources/data`.
Based on a specific company's data, the `stage02.py` script creates a latex
document structure and creates custom JSON files `fund_data.json` and
`calc_data.json`. The JSON files initially have placeholders that are replaced
with extracted data from the company JSON files. These custom JSON files form
the backend, so in case the API changes, it is quite straight forward to adapt
the project. Stage 2 can be triggered as follows:

```bash
./stage02.py -i <isin>
```

This stage uses the `json2latex`[2] Python package in order to make it possible
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

The documentation for this project is located in the `src/docs` directory and
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

The linters for Markdown files are:

- `mdl`

### JSON linter

The linters for JSON files are:

- `jsonlint-php`

### Latex linter

The linters for Latex files are:

- `chktex`
- `lacheck`

### Bash linter

The linters for Bash files are:

- `shellcheck`

### Python linter

The linters for Python files are:

- `pycodestyle`
- `pylint`
- `pyflakes`
- `mccabe`

## Unittests

`Pytest` is used as the unit testing framework for this project.

### Coverage

The unit test stage is orchestrated via the `coverage` Python module.

Current code coverage: 27%

## Handbook

In the `/demo` folder, there is a handbook PDF file that explains the different
ratios and metrics used in the company/stock analysis. This way, the explanatory
texts could be removed from the actual analysis.

## CI/CD

We leverage GitHub Actions for CI/CD with the following jobs:

- Test job: unit tests the python functions
- Build PDF job: execute stage 1 and stage 2 of the analysis pipeline
- Build Handbook job: generate the handbook PDF

The CI/CD pipeline makes sure that the codebase does not break.

## Development Suggestions

My development process for a new feature is as follows:

1. For a new feature a `development` branch is opened. This keeps the `main`
branch clean.
2. Implement new feature.
3. Execute linters and unit tests locally to validate that code base is not
broken.
4. Execute a CI/CD pipeline manually for the `development` branch.
5. If CI/CD turns green, update the Readme and changelog.
6. Rebase `main` branch and add version tag.
7. Push on `main` will trigger CI/CD pipeline.
8. When green, you can delete the `development` branch.

## TODO

- Add more unit test Python functions
- Clean code based on linter scripts

## Sources

[1] [EOD](https://eodhistoricaldata.com/)

[2] [JSON2Latex](https://pypi.org/project/json2latex/)
