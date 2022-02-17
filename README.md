# Investing Calculator

## Introduction 

This system should provide a procedural way to analyse financial data of a 
company. It should provide a financial analysis. The analysis is integrated into 
an analysis pipeline.

## System Architecture

![Architecture Diagram](./images/workflow.png)

## Description

In the flowchart you can see the analysis pipeline. It consists of two stages: 
the first stage pulls the financial data form the Web API, the second stage does
a financial analysis and creates a PDF. At the end of the pipeline, a PDF is 
generated with the corresponding financial data included. Additional custom text 
additions can be included.

## Components

- Python Script X (`stage01.py`): Get financial data from the Web API and put it 
into the data store.

- Python Script Y (`stage02.py`): Transform latex template into company-specific 
latex template and replace placeholders with the actual data from the JSON file. 

- Latex Template with placeholders: The final company PDF will always have the 
same structure and content. It is only the financial data that will be different.
This template will be used to create company-specific templates.

- Python Script Z (`search_api.py`): Uses the search API to get the ticker and 
exchangeID that is needed for the EOD Fundamental Data API. Normally the script 
`stage01.py` would be triggered first. If there is no entry for the ISIN in the 
`stocks.json` file, we can use this script to get the symbol and exchange ID of 
the stock. The data is uniquely identified by the ISIN and will be used by 
`stage01.py` and `stage02.py`.

## Stage 0: Preparation 

In this first step, we prepare the directory structure for the upcoming stages
and check if there is an entry for the ISIN of the company in the `stocks.json`
file. This file documents for each ISIN the corresponding code and exchange ID
that is needed for the fundamental data API. The fundamental data is stored in
the `data.json` file and the latex template is created. Each company is uniquely
identified by the ISIN as the folder name.

## Stage 1: Getting financial data and store it locally

1. We have a Python Script X which queries a Web API for financial data and gets
the requested financial data as a response. The data is formatted as JSON.

2. The Python Script X writes this data into a JSON file located in the
company-specific directory.

## Stage 2: PDF generation

There are two types of placeholders in the Latex template:

- Placeholder type A: These placeholders are used as keys into the company JSON
file and will be replaced by looked up data.

- Placeholder type B: These placeholders are reserved for calculated data, i.e. 
data that is not directly readable from the JSON file, but needs to be calculated
with the data retrieved from this file. 

These two placeholder types should be distinguished with a different prefix.
 
1. The Python Script Y parses the Company latex template and uses the placeholders 
of type A in the Latex template as key to look up the corresponding values in the JSON file.
The looked up data is then fed back into the Latex template to replace the 
placeholders of type A. We end up with a company latex directory that has the
placeholders of type A replaced with the corresponding values from the JSON file.
Only placeholders of type B are left.

2. The looked up data from the previous step is also used to calculate ratios 
and do the analysis. Any data that is generated as part of this step is also fed 
back into the Latex template to replace the corresponding placeholders of type B. 
We end up with a company latex directory that has no placeholders left.

## Stage 3: Manual Edit

After stage 2, we have all the financial data and analysis completed and the 
placeholders of the Latex template have been replaced by the corresponding real
data. As part of the analysis, the user/analyst has the option to manually edit
the corresponding Latex template. It is possible to manually trigger a PDF build. 

## What to use as Data Store?

There are multiple different choices available:  

- PickleDB[1]: A simple key-value store. It is light-weight and fast. The 
problem with PickleDB is that it is not necessarily best suited when having 
multiple value points for different years on the same key. For example, we would
have 10 different values for earnings (i.e. the key).

- Another DB system: The problem is that I want a rather light-weight solution.
DB systems might grow too much and take up too much space. The problem would 
also be that it takes another computation step between accessing the Web API to 
get the financial data and putting the data into the database.

- CSV file: This would be a rather good solution and many APIs offer CSV file 
output. The problem I see here is that I don't know how CSV handles data with 
different length. As far as I understand it, the parsing is also not that 
straight-forward.

- JSON file: This is my current optimal solution. The APIs I am interested in 
all provide the financial data as JSON. JSON can be internally handled as a 
dictionary with Python and thus access is rather straight-forward.

## What Web API to use to get the financial data?

There are multiple different choices available:

- ALPHA Vantage[2]: This API provides free financial data, including historical
data from many different companies and it is for free. The problem with this 
API is literally that the data does not reach back far enough in order to do a
proper financial historical analysis, where I would need to look back up to 10 
years or so.

- EOD Historical Data[3]: This API really provides all the necessary fundamental
historical data that I would need for a proper analysis. It reaches back as far 
as 30 years and provides the data in JSON. The problem here really is the 
pricing.

More stock market APIs can be found at [4].

## Why do we also use other information than only the ticker symbol for the directory creation?

The problem with simply using stock ticker symbols is that it is easy to lose 
overview when there are a lot of ticker symbols. So, the more information is already
included in the file path, we can more easily find companies that compete etc.

## How to make the architecture more independent from the Web API?

Different APIs will probably use different key names in their data/JSON files. 
To cope with this situation, it might be useful to separate the system into a 
frontend and backend:

- Frontend: Get the financial data from the Web API into a JSON file.

- Glue code: Transforms the API-specific data into a intermediate representation.
This intermediate representation could another JSON file that is created from a 
JSON template with placeholders that is filled with data from the original JSON 
file. I would need a API-specific mapping from key names of the original JSON 
file to the key names of the intermediate representation. This intermediate 
representation is API-agnostic. That way it is possible to define a self-contained
backend that. So if the API changes for some reason or the key names change in 
the original JSON file, we would only need to update the mapping but the backend 
itself does not have to be adapted.

- Backend: Replace the placeholders of the Latex template with the values of the
intermediate representation. Calculate the ratios to execute the analysis and 
generate the PDF.

All this is currently not implemented. I focus on the EOD API for now.

## Sources

[1] [PickleDB](https://pythonhosted.org/pickleDB/)

[2] [AlphaVantage](https://www.alphavantage.co/)

[3] [EOD](https://eodhistoricaldata.com/)

[4] [StockMarketAPIs](https://geekflare.com/best-stock-market-api/)

