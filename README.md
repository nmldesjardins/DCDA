# DCDA
Recidivism analysis for Deschutes County District Attorney

# Purpose
These modules can be used to extract and combine data from the Microsoft SQL server, 
engineer features, and conduct initial analyses. The original analyses were conducted
on a remote desktop with limiting processing power, which severly limited the complexity
of the data and the analyses.

# Modules

## connect.py
* Opens the connection to the SQL server

## dflonglong.py
* Extracts and joins filtered tables from SQL
* Stores the data in a pandas dataframe
* Closes the connection to the SQL server

## featureDicts.py, featureDictsTrunc.py
* Defines dictionaries for labeling data
* featureDicts provides labels for the whole dataset
* featureDictsTrunc provides truncated labels based on the top 19 crimes

## featurefunctions.py
* Defines functions used to create features

## createfeatures.py, truncatedFeatures.py
* Cleans up natural lanugage data
* Call featurefunctions and featureDicts to create features
* createfeatures generates features for the entire dataset
* truncatedFeatures:
    * creates a truncated dataset that only includes the top 19 crime categories
    * generates features for the top 19 crimes only

## restructure.py
* Calls the dataframe produced by truncatedFeatures (but could be adjusted to use createfeatures instead)
* Restructures the data to be long by count
    * Each row is a count
    * There are multiple counts for each case, and multiple cases for each person
    * There are multiple sentencing conditions for each count; this file combines them into a single row

## createFirstCrimes.py
* Generates a dataset that includes just the first cases in the database for each defendant
* Calls from truncatedFeatures -> restructure
* Only includes first crimes among defendants who were charged with one of the top crimes
* Creates new features for analysis

## preliminaryAnalyses
* Produces preliminary analyses examining the recidivism rate by
    * top crimes
    * sentencing category
    * demographic group
* Estimates preliminary logistic regressions predicting recidivism from each group of features
* Estimates a preliminary ExtraTreesClassifier to establish the importance of each feature