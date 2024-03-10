# Backlog

## Rewrite the python code base as classes

- prerequisite: have test coverage in place, so refactoring does not become a
  nightmare
- rewrite the entire python code as classes not these functions
- probably have to rewrite also test cases

## Add jinja templating to json files

- current state: I use a complicated mechanism with sed and regex
- goal: use jinja templates in JSON files to avoid sed scheme
- motivation: sed is complicated an no one understands anything when looking at
  the code 2 years later, with jinja can simply call python functions

## Split stages into tools

- instead of stage01 and stage02 create actual tools and have python code
  separately

## Move testing environment into docker containers

- current state: only unit tests, so it doesn't matter if I run it on the host
  directly or in a container
- goal: put system tests in containers to avoid doing something wrong with the
  file system

## Use docopt package in python code

- current state: I parse the command line arguments
- goal: use docopt python package
- motivation: it's cleaner

## Automatically rank different stocks based on metrics

- outcome: get list of interesting stocks
- analyze the `calc_data.json` for these companies and create basically grading
  system and rank them
- current state: still have to go through all the companies myself
- goal: get list of companies ranked by metrics, e.g. each metric gets a
  certain range that is considered good, if company good for metric give 1
  point, otherwise 0 points -> rank the companies by the point -> immediately
  know which companies are financially sound and look into them

## Write script that checks whether/when to buy/sell a stocks

- tool will run regularly in background (cron job) and tell which stocks should
  be bought and sold
- write the stocks you are interested in and the price you want to buy them at
  into a file called `interested`
- write the stocks you are invested in and the price you want to sell them at
  into a file called `invested`
- 1st step: tool plugs into real-time API to check daily stock price and will
  compare with set price in `interested` or `invested`, if criteria met, put
  matching stocks in `interested` into `candidates_to_buy` and matching stocks
  in `invested` into `candidates_to_sell`
- then use the 3 tools: MACD, slow stochastics and moving average to decide
  on correct time to sell the stocks in `candidates_to_sell` or to buy the
  stocks in `candidates_to_buy`

## Validate how my pipeline would have worked in the past

- Problem: My strategy is based on long-term investment, i.e. there is no easy
  way to predict how my strategy works without waiting for multiple years.
- Idea: What we could do is to use my pipeline on data from the past and see
  how my predictions would have worked if I would have invested back then
  according to the pipeline output.
- Use my pipeline on data from a few years back and check whether my
  predictions developed over time to get a good feeling for how good my
  process can help in figuring out good stock picks
