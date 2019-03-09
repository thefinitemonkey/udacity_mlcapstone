# Machine Learning Engineer Nanodegree
## Capstone Project
Doug Brown  
March 9, 2019

## I. Definition

### Project Overview
This project originates from a Kaggle challenge that is available at https://www.kaggle.com/c/tmdb-box-office-prediction

The entertainment industry is regularly creating new content. This is a heavy investment, with the businesses producing the content continually seeking ways to optimize their returns. Using predictive analytics is one way companies are using to help refine their decision making processes. The amount of data available to entertainment businesses for each property they create is vast, so if they can reach into that data and determine winning formulas they may be able to improve their revenue.

Netflix is a perfect example of this type of behavior. Based on their user's viewing habits they determined that their audience had high preferences for certain actors, writers, directors, and genres. As an experiment with their data they took this information and put a specific selection of individuals from these areas together to create a show. There was no concept for the show, just the desire to get a particular combination of people together with the expectation, based on the analytics, that the results would be a hit. From that experiment the series _House of Cards_ was produced.

For this project there will be work done to see if similar insights can be made regarding movies produced and distributed through theaters. This is a global market that all movie makers are continually seeking to create greater reach in terms of audience and revenue, and the public domain data available for this kind of exercise is considerable.

### Problem Statement
The quesion then is, given all the relevant, historical data for a selection of movies, can a model be created for predicting the performance of other films based on similar data. Performance in this case is measured by box office revenue, which is the true metric by which studios measure the success of their products.

From the Kaggle competition a dataset of movies is made available. There are ~3000 movies in the dataset that crosses years, genres, countries, languages, directors, actors, and practically every other descriptive data related to each film. Ideally, a model can be constructed that can consider these factors and use them to make a well-educated guess about the likely revenue for a film.

At a high level, this problem will be approached by
* Acquiring the data
* Doing any necessary pre-processing of the data
* Splitting the data into training and testing sets
* Developing the model based on predicting revenue
* Training the model using the training dataset
* Evaluating the model using the testing dataset
* Drawing conclusions regarding possible improvements to the model

### Metrics
Judging the success of the model will be done using the Kaggle competition metric of Root Mean Log Squared Error. Since we are dealing strictly with financial outcomes (revenue) we can make good comparisons based on the disparity between our predictions and true results. Root mean log squared error will allow for taking a group of predictions and generally evaluating their accuracy again the actual results. Additionally, the Root Mean Square Log Error avoids penalizing large differences between results if the numbers being considered are also large. So small differences between small numbers and large differences between large numbers will be treated similarly.

No model will ever be perfectly able to predict the outcomes, which would require perfect knowledge of all variables both inside and outside the control of the movie production efforts. However, a model that can provide good, general guidance should be possible, and this metric will let us gauge this model.


## II. Analysis

### Data Exploration
The data for this project is very robust. It comes in the form of a csv file culled from The Movie Database and hs 3000 movies. The dataset provided contains the following attributes (see the appendix for a sample data record):
* belongs_to_collection: This field contains an array of data objects describing what series the film belongs to, including the unique series ids and names, if it is part of a series (i.e. _Star Wars_, _Jurassic Park_, etc.)
* budget: This field is an integer value representing the production budget for the film
* genres: This field contains an array of data objects describing the genres with which the film is categorized, including the unique genres ids and names
* homepage: This field contains a string representing the url of the marketing homepage for the film, if one existed
* imdb_id: The film's id within the Internet Movie Database index
* original_language: The string value of the ISO language value for the spoken language in the film's original distribution
* original_title: The string value of the title originally used for the film, which may be different than the commonly known title
* overview: The string representation of the film's summary
* popularity: A floating point value representing the popularity of the film
* poster_path: A string representing the url for an image of the movie's poster, if one is available
* production_companies: This field contains an array of objects describing the production companies involved in the film, including the unique id and name of the company
* production_countries: This field contains an array of objects describing the countries in which the film was produced, including the ISO id and name of the country
* release_date: A string representation of the date on which the film was originally released
* runtime: An intiger value for the runtime of the film in minutes
* spoken_languages: This is an array of objects representing the languages spoken in the film, with each item containing both the ISO id and name of the language
* status: A string representation of the film's status, either released or rumored
* tagline: A string representation of the marketing tagline for the film if there was one
* title: A string repreentation of the film's title at release
* keywords: This is an array of objects representing the keywords associated with the film, with each object containing both the unique id for the keyword and the string for the keyword
* cast: This is an array of objects representing all the actors associated with the film, with each object containing both the unique id and name of the actor along with the order of billing for each
* crew: This is an array of objects representing all the crew members associated with the film with each object containing both the unique id and name of the crew member along with their role in the film's production
* revenue: An integer value representing the global box-office revenue in US dollars

Each of the fields containing arrays of objects are presented as string values with the appearance of a JSON array. For example **[{'id': 313576, 'name': 'Hot Tub Time Machine Collection', 'poster_path': '/iEhb00TGPucF0b4joM1ieyY026U.jpg', 'backdrop_path': '/noeTVcgpBiD48fDjFVic1Vz7ope.jpg'}]**

Given that this format actually represents possibly multiple values of significant interest relating to the film it cannot be analyzed as-is. These field types will definitely need to be transformed. Fields such as _keywords_, _crew_ and _actors_ likely represent thousands of values each. The _actors_ field does provide an attribute indicating the order of billing for cast members, so in this case how many actors are being considered could be reduced if we only consider the few top-billed members of each film. These values cannot be directly one-hot encoded, so additional work will be required and all null instances will need to be filled as 0.

All string fields require some type of transformation to be useful in analysis. Fields such as _tagline_, _overview_, and the transformed _keywords_ could be one-hot encoded for consideration. Again, this will certainly lead to many thousands of data points.

The date field is a string and will require transformation into numeric values that are useful for analysis. In this case I will choose to represent them as _week_ and _year_. The _week_ will represent the number of the week (0-51) in which each film was released. Since films are commonly released on a Friday it is assumed it will be more useful to know which week the film was released rather than which specific month / day.

Some fields, such as imdb_id, have no meaningful data for doing predictive analytics. The following fields will be dropped from consideration:
* imdb_id: This is an index key to another database and is not meaningful
* poster_path: This is a url for a movie poster which will not be visually analyzed here
* status: Since all films are assumed to have been released this is ignored (three films were mis-categorized as rumored)

Some outliers, particulary for budget and revenue numbers, do exist within the data. These are represented as decimal values rather than integers, and are typically of values smaller than 100. Review of other data sources shows that in these cases the numbers represent millions of dollars, so in these cases the numbers are corrected.

There are also movies within the dataset that are missing revenue, budget, and runtime data. These values have been acquired from other public sources and will be manually corrected within the data at runtime.



### Exploratory Visualization

Without pre-processing the data, there is very little data that can be visually analyzed. A quick pairplot on the following will let us see if there might be any strength between:
* budget
* popularity
* runtime
* revenue

![](https://github.com/thefinitemonkey/udacity_mlcapstone/blob/master/images/pairplot.png)

It does appear that there may be a linear correlation between the budget and revenue. This intuitively seems reasonable, as a film with a higher budget might generally be thought of as having a higher quality. It also appears that there may be a correlation between the runtime and revenue. This takes more the shape of a bell curve however. Films around two hours appear to generally do best in terms of revenue, falling off on either side of that. Popularity and revenue seem to have very little interaction however.

### Algorithms and Techniques
I will be using two different types of regression models for this analysis. The first will be a Linear Regression and will be used to obtain a benchmark. The second is a Decision Tree and will be used for more complex modeling. In both cases a shuffle split will be used for training purposes.

#### Linear Regression
This is a linear approach to modeling relationships between the dependent variable, in this case revenue, and one or more independent variables. These relationship are modeled using linear predictor function where the model parameters are estimated from the data provided. The model focuses on conditional probability distribution of responses given the data provided. This is useful for prediction with a smaller set of numeric data, which is what we have in the unprocessed dataset.

#### Decision Tree
Decision tree models build regressions in the form of a tree structure. The dataset is broken into incrementally smaller subsets, which informs the incremental development of the questions that make up the tree. The tree itself is then comprised of _decision nodes_ and _leaf nodes_. Each decision node will have two or more branches, each of which will lead to either another decision node or a leaf node. The leaf nodes represent final determinations made by the model based on the data provided.

#### Shuffle Split
Since training requires that true outcomes be available in advance, it is important to split the data into training and testing sets and to separate the known outcomes from the predictive data. This does two things:
1. It prevents the model from memorizing all the data and not generalizing the model well. This is known as over-fitting.
2. The models should not have access to the known outcomes while training. It sounds obvious, but is important to keep in mind. The model will make predictions while it is learning and then compare against the known outcomes. This will further inform the models learning, depending on the model used.

### Benchmark
There is no default benchmark value provided for this particular exercise. So creating a benchmark is required to allow comparison as a more complex model is built out.

Using the predetermined linear regression and a custom scorer for Root Mean Square Log Error a model was generated for the unprocessed data. Since this is the scoring mechanism used for the Kaggle competition it is used here as well. As noted earlier, Root Mean Square Log Error prevents large differences between large numbers from being penalized different from smaller differences between smaller numbers. This is important int the context of this data as some films have worldwide revenue of close to $1 billion US.

The best estimator was generated and run against the test data split from the training set. A look at the first 20 results shows that the model predicted several films to have revenues significantly in the negative amounts. The final score from the benchmark modeling was **1.6401099366269307**.


## III. Methodology
_(approx. 3-5 pages)_

### Data Preprocessing
In this section, all of your preprocessing steps will need to be clearly documented, if any were necessary. From the previous section, any of the abnormalities or characteristics that you identified about the dataset will be addressed and corrected here. Questions to ask yourself when writing this section:
- _If the algorithms chosen require preprocessing steps like feature selection or feature transformations, have they been properly documented?_
- _Based on the **Data Exploration** section, if there were abnormalities or characteristics that needed to be addressed, have they been properly corrected?_
- _If no preprocessing is needed, has it been made clear why?_

### Implementation
In this section, the process for which metrics, algorithms, and techniques that you implemented for the given data will need to be clearly documented. It should be abundantly clear how the implementation was carried out, and discussion should be made regarding any complications that occurred during this process. Questions to ask yourself when writing this section:
- _Is it made clear how the algorithms and techniques were implemented with the given datasets or input data?_
- _Were there any complications with the original metrics or techniques that required changing prior to acquiring a solution?_
- _Was there any part of the coding process (e.g., writing complicated functions) that should be documented?_

### Refinement
In this section, you will need to discuss the process of improvement you made upon the algorithms and techniques you used in your implementation. For example, adjusting parameters for certain models to acquire improved solutions would fall under the refinement category. Your initial and final solutions should be reported, as well as any significant intermediate results as necessary. Questions to ask yourself when writing this section:
- _Has an initial solution been found and clearly reported?_
- _Is the process of improvement clearly documented, such as what techniques were used?_
- _Are intermediate and final solutions clearly reported as the process is improved?_


## IV. Results
_(approx. 2-3 pages)_

### Model Evaluation and Validation
In this section, the final model and any supporting qualities should be evaluated in detail. It should be clear how the final model was derived and why this model was chosen. In addition, some type of analysis should be used to validate the robustness of this model and its solution, such as manipulating the input data or environment to see how the model’s solution is affected (this is called sensitivity analysis). Questions to ask yourself when writing this section:
- _Is the final model reasonable and aligning with solution expectations? Are the final parameters of the model appropriate?_
- _Has the final model been tested with various inputs to evaluate whether the model generalizes well to unseen data?_
- _Is the model robust enough for the problem? Do small perturbations (changes) in training data or the input space greatly affect the results?_
- _Can results found from the model be trusted?_

### Justification
In this section, your model’s final solution and its results should be compared to the benchmark you established earlier in the project using some type of statistical analysis. You should also justify whether these results and the solution are significant enough to have solved the problem posed in the project. Questions to ask yourself when writing this section:
- _Are the final results found stronger than the benchmark result reported earlier?_
- _Have you thoroughly analyzed and discussed the final solution?_
- _Is the final solution significant enough to have solved the problem?_


## V. Conclusion
_(approx. 1-2 pages)_

### Free-Form Visualization
In this section, you will need to provide some form of visualization that emphasizes an important quality about the project. It is much more free-form, but should reasonably support a significant result or characteristic about the problem that you want to discuss. Questions to ask yourself when writing this section:
- _Have you visualized a relevant or important quality about the problem, dataset, input data, or results?_
- _Is the visualization thoroughly analyzed and discussed?_
- _If a plot is provided, are the axes, title, and datum clearly defined?_

### Reflection
In this section, you will summarize the entire end-to-end problem solution and discuss one or two particular aspects of the project you found interesting or difficult. You are expected to reflect on the project as a whole to show that you have a firm understanding of the entire process employed in your work. Questions to ask yourself when writing this section:
- _Have you thoroughly summarized the entire process you used for this project?_
- _Were there any interesting aspects of the project?_
- _Were there any difficult aspects of the project?_
- _Does the final model and solution fit your expectations for the problem, and should it be used in a general setting to solve these types of problems?_

### Improvement
In this section, you will need to provide discussion as to how one aspect of the implementation you designed could be improved. As an example, consider ways your implementation can be made more general, and what would need to be modified. You do not need to make this improvement, but the potential solutions resulting from these changes are considered and compared/contrasted to your current solution. Questions to ask yourself when writing this section:
- _Are there further improvements that could be made on the algorithms or techniques you used in this project?_
- _Were there algorithms or techniques you researched that you did not know how to implement, but would consider using if you knew how?_
- _If you used your final solution as the new benchmark, do you think an even better solution exists?_

-----------

**Before submitting, ask yourself. . .**

- Does the project report you’ve written follow a well-organized structure similar to that of the project template?
- Is each section (particularly **Analysis** and **Methodology**) written in a clear, concise and specific fashion? Are there any ambiguous terms or phrases that need clarification?
- Would the intended audience of your project be able to understand your analysis, methods, and results?
- Have you properly proof-read your project report to assure there are minimal grammatical and spelling mistakes?
- Are all the resources used for this project correctly cited and referenced?
- Is the code that implements your solution easily readable and properly commented?
- Does the code execute without error and produce results similar to those reported?

## Appendix

### Sample Data
The following is the data record for one film in the dataset. If you like _Hot Tub Time Machine_ then you'll like this sample data.  :)

1	[{'id': 313576, 'name': 'Hot Tub Time Machine Collection', 'poster_path': '/iEhb00TGPucF0b4joM1ieyY026U.jpg', 'backdrop_path': '/noeTVcgpBiD48fDjFVic1Vz7ope.jpg'}]	14000000	[{'id': 35, 'name': 'Comedy'}]		tt2637294	en	Hot Tub Time Machine 2	When Lou, who has become the "father of the Internet," is shot by an unknown assailant, Jacob and Nick fire up the time machine again to save their friend.	6.575393	/tQtWuwvMf0hCc2QR2tkolwl7c3c.jpg	[{'name': 'Paramount Pictures', 'id': 4}, {'name': 'United Artists', 'id': 60}, {'name': 'Metro-Goldwyn-Mayer (MGM)', 'id': 8411}]	[{'iso_3166_1': 'US', 'name': 'United States of America'}]	2/20/15	93	[{'iso_639_1': 'en', 'name': 'English'}]	Released	The Laws of Space and Time are About to be Violated.	Hot Tub Time Machine 2	[{'id': 4379, 'name': 'time travel'}, {'id': 9663, 'name': 'sequel'}, {'id': 11830, 'name': 'hot tub'}, {'id': 179431, 'name': 'duringcreditsstinger'}]	[{'cast_id': 4, 'character': 'Lou', 'credit_id': '52fe4ee7c3a36847f82afae7', 'gender': 2, 'id': 52997, 'name': 'Rob Corddry', 'order': 0, 'profile_path': '/k2zJL0V1nEZuFT08xUdOd3ucfXz.jpg'}, {'cast_id': 5, 'character': 'Nick', 'credit_id': '52fe4ee7c3a36847f82afaeb', 'gender': 2, 'id': 64342, 'name': 'Craig Robinson', 'order': 1, 'profile_path': '/tVaRMkJXOEVhYxtnnFuhqW0Rjzz.jpg'}, {'cast_id': 6, 'character': 'Jacob', 'credit_id': '52fe4ee7c3a36847f82afaef', 'gender': 2, 'id': 54729, 'name': 'Clark Duke', 'order': 2, 'profile_path': '/oNzK0umwm5Wn0wyEbOy6TVJCSBn.jpg'}, {'cast_id': 7, 'character': 'Adam Jr.', 'credit_id': '52fe4ee7c3a36847f82afaf3', 'gender': 2, 'id': 36801, 'name': 'Adam Scott', 'order': 3, 'profile_path': '/5gb65xz8bzd42yjMAl4zwo4cvKw.jpg'}, {'cast_id': 8, 'character': 'Hot Tub Repairman', 'credit_id': '52fe4ee7c3a36847f82afaf7', 'gender': 2, 'id': 54812, 'name': 'Chevy Chase', 'order': 4, 'profile_path': '/svjpyYtPwtjvRxX9IZnOmOkhDOt.jpg'}, {'cast_id': 9, 'character': 'Jill', 'credit_id': '52fe4ee7c3a36847f82afafb', 'gender': 1, 'id': 94098, 'name': 'Gillian Jacobs', 'order': 5, 'profile_path': '/rBnhe5vhNPnhRUdtYahBWx90fJM.jpg'}, {'cast_id': 10, 'character': 'Sophie', 'credit_id': '52fe4ee7c3a36847f82afaff', 'gender': 1, 'id': 1159009, 'name': 'Bianca Haase', 'order': 6, 'profile_path': '/4x3nbtD8q8phAJPmoGWXPvz0iM.jpg'}, {'cast_id': 11, 'character': 'Kelly', 'credit_id': '5524ec51c3a3687df3000dbb', 'gender': 1, 'id': 86624, 'name': 'Collette Wolfe', 'order': 7, 'profile_path': '/aSD4h5379b2eEw3bLou9ByLimmq.jpg'}, {'cast_id': 13, 'character': 'Brad', 'credit_id': '5524ec8ec3a3687ded000d72', 'gender': 2, 'id': 466505, 'name': 'Kumail Nanjiani', 'order': 9, 'profile_path': '/x4nAztHY72SVciRfxEsbhIVTsIu.jpg'}, {'cast_id': 14, 'character': 'Courtney', 'credit_id': '5524ec9bc3a3687df8000d13', 'gender': 1, 'id': 70776, 'name': 'Kellee Stewart', 'order': 10, 'profile_path': '/w3xmsEPmJc1Cf0dQ4aIn8YmlHbk.jpg'}, {'cast_id': 15, 'character': 'Terry', 'credit_id': '5524eca892514171cb008237', 'gender': 2, 'id': 347335, 'name': 'Josh Heald', 'order': 11, 'profile_path': '/pwXJIenrDMrG7t3zNfLvr8w1RGU.jpg'}, {'cast_id': 16, 'character': 'Susan', 'credit_id': '5524ecb7925141720c001116', 'gender': 0, 'id': 1451392, 'name': 'Gretchen Koerner', 'order': 12, 'profile_path': '/muULPexCTJGyJba4yKzxronpD50.jpg'}, {'cast_id': 17, 'character': 'Herself', 'credit_id': '5524ecc3c3a3687ded000d74', 'gender': 1, 'id': 98879, 'name': 'Lisa Loeb', 'order': 13, 'profile_path': '/bGqg58ca0bZR38z9HliUMmeNGE.jpg'}, {'cast_id': 18, 'character': 'Herself', 'credit_id': '5524ecd3c3a3687e11000ed3', 'gender': 1, 'id': 1394648, 'name': 'Jessica Williams', 'order': 14, 'profile_path': '/A4syKjkcYB92wLEhH0c0hC3BCpz.jpg'}, {'cast_id': 19, 'character': 'Himself', 'credit_id': '5524ece6925141718d001009', 'gender': 0, 'id': 1451393, 'name': 'Bruce Buffer', 'order': 15, 'profile_path': None}, {'cast_id': 20, 'character': 'Shot Girl', 'credit_id': '5524ecf5c3a3687e08000dc2', 'gender': 0, 'id': 1451394, 'name': 'Mariana Paola Vicente', 'order': 16, 'profile_path': '/ckPllza8624UHWGHCbLShkLxCD1.jpg'}, {'cast_id': 33, 'character': 'Choozy Doozy Host', 'credit_id': '555844da9251412afe0013a9', 'gender': 2, 'id': 2224, 'name': 'Christian Slater', 'order': 17, 'profile_path': '/3ElLWjnvchMS6Q4cIQOK8QNAoMG.jpg'}, {'cast_id': 35, 'character': 'Gary Winkle', 'credit_id': '55872027c3a3683853005074', 'gender': 0, 'id': 185805, 'name': 'Jason Jones', 'order': 18, 'profile_path': '/aIoCw6vo8AGMdsQRAI5g2t0yJT3.jpg'}, {'cast_id': 36, 'character': 'Bridesmaid', 'credit_id': '55efe971c3a368090c00cd1b', 'gender': 0, 'id': 1507448, 'name': 'Olivia Jordan', 'order': 19, 'profile_path': '/szMukAEiIDeasel0lvyaeyKuych.jpg'}, {'cast_id': 37, 'character': 'Christine', 'credit_id': '55efe980c3a36871bf008176', 'gender': 1, 'id': 1334091, 'name': 'Christine Bently', 'order': 20, 'profile_path': '/oUZltnGa55OXE52hfyPTfCshuNy.jpg'}, {'cast_id': 38, 'character': 'Excited Girl', 'credit_id': '55efe98e9251413e3201d316', 'gender': 0, 'id': 557803, 'name': 'Stacey Asaro', 'order': 21, 'profile_path': '/qTPdlr1dXf3kNdyHuDsgtGC0HCC.jpg'}, {'cast_id': 64, 'character': 'Adam (uncredited)', 'credit_id': '58f2135ac3a3682e95008b91', 'gender': 2, 'id': 3036, 'name': 'John Cusack', 'order': 22, 'profile_path': '/uKydQYuZ9TnCzvbQLtj6j98vWAT.jpg'}, {'cast_id': 65, 'character': 'J-Bird', 'credit_id': '59ac0240c3a3682cc802c399', 'gender': 2, 'id': 59256, 'name': 'Adam Herschman', 'order': 23, 'profile_path': '/wZMwiuX1DslF6hDS50z9OTN6z1X.jpg'}, {'cast_id': 66, 'character': 'Bridesmaid', 'credit_id': '59ac02cd925141079d02b1b4', 'gender': 1, 'id': 129714, 'name': 'Kisha Sierra', 'order': 24, 'profile_path': None}]	[{'credit_id': '59ac067c92514107af02c8c8', 'department': 'Directing', 'gender': 0, 'id': 1449071, 'job': 'First Assistant Director', 'name': 'Kelly Cantley', 'profile_path': None}, {'credit_id': '52fe4ee7c3a36847f82afad7', 'department': 'Directing', 'gender': 2, 'id': 3227, 'job': 'Director', 'name': 'Steve Pink', 'profile_path': '/myHOgo8mQSCiCAZNGMRdHVr03jr.jpg'}, {'credit_id': '5524ed25c3a3687ded000d88', 'department': 'Writing', 'gender': 2, 'id': 347335, 'job': 'Writer', 'name': 'Josh Heald', 'profile_path': '/pwXJIenrDMrG7t3zNfLvr8w1RGU.jpg'}, {'credit_id': '5524ed2d925141720c001128', 'department': 'Writing', 'gender': 2, 'id': 347335, 'job': 'Characters', 'name': 'Josh Heald', 'profile_path': '/pwXJIenrDMrG7t3zNfLvr8w1RGU.jpg'}, {'credit_id': '5524ed3d92514166c1004a5d', 'department': 'Production', 'gender': 2, 'id': 57822, 'job': 'Producer', 'name': 'Andrew Panay', 'profile_path': None}, {'credit_id': '5524ed4bc3a3687df3000dd2', 'department': 'Production', 'gender': 0, 'id': 1451395, 'job': 'Associate Producer', 'name': 'Adam Blum', 'profile_path': None}, {'credit_id': '5524ed5a925141720c00112c', 'department': 'Production', 'gender': 2, 'id': 52997, 'job': 'Executive Producer', 'name': 'Rob Corddry', 'profile_path': '/k2zJL0V1nEZuFT08xUdOd3ucfXz.jpg'}, {'credit_id': '5524ed85c3a3687e0e000f56', 'department': 'Production', 'gender': 0, 'id': 62807, 'job': 'Executive Producer', 'name': 'Ben Ormand', 'profile_path': None}, {'credit_id': '5524ed9fc3a3687e0e000f59', 'department': 'Sound', 'gender': 2, 'id': 23486, 'job': 'Original Music Composer', 'name': 'Christophe Beck', 'profile_path': '/2fnJUmCk6IEpVIptpYaUk31epHx.jpg'}, {'credit_id': '5524eda6c3a3687e03000d28', 'department': 'Camera', 'gender': 2, 'id': 6117, 'job': 'Director of Photography', 'name': 'Declan Quinn', 'profile_path': None}, {'credit_id': '5524edb4925141720c00113d', 'department': 'Editing', 'gender': 0, 'id': 1451396, 'job': 'Editor', 'name': 'Jamie Gross', 'profile_path': None}, {'credit_id': '5524edc1925141727600102e', 'department': 'Production', 'gender': 0, 'id': 22219, 'job': 'Casting', 'name': 'Susie Farris', 'profile_path': None}, {'credit_id': '5524edd192514171cb008257', 'department': 'Art', 'gender': 0, 'id': 1002643, 'job': 'Production Design', 'name': 'Ryan Berg', 'profile_path': None}, {'credit_id': '555ad9be9251411e5b00d485', 'department': 'Production', 'gender': 2, 'id': 57431, 'job': 'Executive Producer', 'name': 'Matt Moore', 'profile_path': None}, {'credit_id': '5677e93bc3a36816890087dc', 'department': 'Directing', 'gender': 0, 'id': 1551818, 'job': 'Script Supervisor', 'name': 'Nicole Garcea', 'profile_path': None}, {'credit_id': '5677e96a92514179e10093d0', 'department': 'Production', 'gender': 0, 'id': 1551819, 'job': 'Production Coordinator', 'name': 'Jason Salzman', 'profile_path': None}, {'credit_id': '5677e98492514179d2008cd9', 'department': 'Costume & Make-Up', 'gender': 0, 'id': 1422996, 'job': 'Costume Design', 'name': 'Carol Cutshall', 'profile_path': None}, {'credit_id': '5677e9d5c3a368168e009414', 'department': 'Art', 'gender': 2, 'id': 500199, 'job': 'Set Decoration', 'name': 'Tim Cohn', 'profile_path': None}, {'credit_id': '5677f89d9251417845001a61', 'department': 'Costume & Make-Up', 'gender': 0, 'id': 1527917, 'job': 'Hair Department Head', 'name': 'Voni Hinkle', 'profile_path': None}, {'credit_id': '5677f8b392514179dd0089fb', 'department': 'Costume & Make-Up', 'gender': 0, 'id': 1431554, 'job': 'Makeup Department Head', 'name': 'Remi Savva', 'profile_path': None}, {'credit_id': '5677f8d1c3a3681689008a4b', 'department': 'Art', 'gender': 0, 'id': 66495, 'job': 'Art Direction', 'name': 'Jason Baldwin Stewart', 'profile_path': None}, {'credit_id': '5677f8eec3a3681685008dd5', 'department': 'Production', 'gender': 0, 'id': 1412466, 'job': 'Production Supervisor', 'name': 'Korey Budd', 'profile_path': None}, {'credit_id': '5677f90a9251417845001a7d', 'department': 'Sound', 'gender': 0, 'id': 1401562, 'job': 'Sound Re-Recording Mixer', 'name': 'Gary C. Bourgeois', 'profile_path': None}, {'credit_id': '5677f91e9251417845001a84', 'department': 'Sound', 'gender': 0, 'id': 1396794, 'job': 'Sound Re-Recording Mixer', 'name': 'Gabriel J. Serrano', 'profile_path': None}, {'credit_id': '5677f938c3a3681680008dd4', 'department': 'Editing', 'gender': 0, 'id': 13168, 'job': 'Dialogue Editor', 'name': 'Victoria Rose Sampson', 'profile_path': None}, {'credit_id': '5677f94e92514179dd008a1f', 'department': 'Sound', 'gender': 0, 'id': 1551839, 'job': 'Production Sound Mixer', 'name': 'Michael B. Koff', 'profile_path': None}, {'credit_id': '5677f968c3a368168e009698', 'department': 'Sound', 'gender': 0, 'id': 113052, 'job': 'Sound Effects Editor', 'name': 'Randall Guth', 'profile_path': None}, {'credit_id': '5677f98dc3a3681685008e02', 'department': 'Crew', 'gender': 2, 'id': 1442535, 'job': 'Stunt Coordinator', 'name': 'Chuck Picerni Jr.', 'profile_path': '/yE5QtXUzcrnCzMRctZL8F5g842B.jpg'}, {'credit_id': '5677f9a692514179dd008a49', 'department': 'Camera', 'gender': 0, 'id': 1437305, 'job': 'Camera Operator', 'name': 'Michael Applebaum', 'profile_path': None}, {'credit_id': '5677f9bd9251417845001aae', 'department': 'Camera', 'gender': 0, 'id': 1401765, 'job': 'Still Photographer', 'name': 'Steve Dietl', 'profile_path': None}, {'credit_id': '5677f9e592514179e7008bf7', 'department': 'Lighting', 'gender': 0, 'id': 1402721, 'job': 'Rigging Gaffer', 'name': 'Tarik Naim Alherimi', 'profile_path': None}, {'credit_id': '5677f9f4c3a368167c0090ed', 'department': 'Lighting', 'gender': 0, 'id': 1402719, 'job': 'Gaffer', 'name': 'Paul Olinde', 'profile_path': None}, {'credit_id': '5677fa21c3a368168e0096ca', 'department': 'Sound', 'gender': 0, 'id': 1551840, 'job': 'Music Supervisor', 'name': 'Steve Griffen', 'profile_path': None}, {'credit_id': '5677fa31c3a3681680008e04', 'department': 'Sound', 'gender': 0, 'id': 1551841, 'job': 'Music Editor', 'name': 'Matt Fausak', 'profile_path': None}, {'credit_id': '5677fa4392514179dd008a76', 'department': 'Sound', 'gender': 0, 'id': 1551840, 'job': 'Music Editor', 'name': 'Steve Griffen', 'profile_path': None}, {'credit_id': '5677fa609251417845001acf', 'department': 'Costume & Make-Up', 'gender': 0, 'id': 1403416, 'job': 'Costume Supervisor', 'name': 'Shonta T. McCray', 'profile_path': None}, {'credit_id': '5677fa8492514179d2008fb3', 'department': 'Camera', 'gender': 0, 'id': 1425831, 'job': 'Steadicam Operator', 'name': 'Mark Karavite', 'profile_path': None}, {'credit_id': '5677fab2c3a3681689008ac3', 'department': 'Camera', 'gender': 0, 'id': 1551842, 'job': 'First Assistant Camera', 'name': 'Joe Waistell', 'profile_path': None}, {'credit_id': '5677faecc3a368168e0096fe', 'department': 'Sound', 'gender': 0, 'id': 58362, 'job': 'Supervising Sound Editor', 'name': 'Michael Hilkene', 'profile_path': None}, {'credit_id': '59ac0368c3a3682c0a02c484', 'department': 'Crew', 'gender': 0, 'id': 1881584, 'job': 'Additional Writing', 'name': 'John Karnay', 'profile_path': None}, {'credit_id': '59ac0411c3a3682bf0028966', 'department': 'Costume & Make-Up', 'gender': 0, 'id': 1431552, 'job': 'Hairstylist', 'name': 'Daina Daigle', 'profile_path': None}, {'credit_id': '59ac0504925141072302b8fb', 'department': 'Costume & Make-Up', 'gender': 0, 'id': 1712001, 'job': 'Makeup Artist', 'name': 'Allison Gordin', 'profile_path': None}, {'credit_id': '59ac0570c3a3682bf0028aac', 'department': 'Costume & Make-Up', 'gender': 0, 'id': 578725, 'job': 'Makeup Artist', 'name': 'Darryl Lucas', 'profile_path': None}, {'credit_id': '59ac05a4925141077e02c97e', 'department': 'Costume & Make-Up', 'gender': 0, 'id': 1463274, 'job': 'Makeup Artist', 'name': 'Annabelle MacNeal', 'profile_path': None}, {'credit_id': '59ac05c6925141076502d106', 'department': 'Costume & Make-Up', 'gender': 0, 'id': 1881586, 'job': 'Makeup Artist', 'name': 'Marina Savva', 'profile_path': None}, {'credit_id': '59ac0615c3a3682c480296aa', 'department': 'Costume & Make-Up', 'gender': 0, 'id': 1406267, 'job': 'Hairstylist', 'name': 'Carl G. Variste', 'profile_path': None}, {'credit_id': '59ac06ba925141076502d1fa', 'department': 'Directing', 'gender': 0, 'id': 1798593, 'job': 'First Assistant Director', 'name': 'Josh King', 'profile_path': None}, {'credit_id': '59ac06f1c3a3682c2202aca0', 'department': 'Art', 'gender': 0, 'id': 1415083, 'job': 'Greensman', 'name': 'Scott C. Bivona', 'profile_path': None}, {'credit_id': '59ac072c925141076502d260', 'department': 'Art', 'gender': 0, 'id': 1881587, 'job': 'Title Designer', 'name': 'Eunha Choi', 'profile_path': None}, {'credit_id': '59ac077c925141077e02cb62', 'department': 'Art', 'gender': 0, 'id': 1585302, 'job': 'Construction Coordinator', 'name': 'Daniel Coe', 'profile_path': None}, {'credit_id': '59ac07e0925141078a02d842', 'department': 'Art', 'gender': 0, 'id': 1495523, 'job': 'Set Designer', 'name': 'Spencer Davison', 'profile_path': None}, {'credit_id': '59ac0862925141072f02cf6f', 'department': 'Art', 'gender': 0, 'id': 1881589, 'job': 'Painter', 'name': 'Sonia L. Garcia', 'profile_path': None}, {'credit_id': '59ac08e0c3a3682bf0028e51', 'department': 'Art', 'gender': 0, 'id': 1424896, 'job': 'Art Department Coordinator', 'name': 'Caleb Guillotte', 'profile_path': None}, {'credit_id': '59ac0920c3a3682c2202af36', 'department': 'Art', 'gender': 0, 'id': 1393375, 'job': 'Leadman', 'name': "Pat A. O'Connor", 'profile_path': None}, {'credit_id': '59ac095592514107af02cc39', 'department': 'Art', 'gender': 0, 'id': 1881592, 'job': 'Set Designer', 'name': 'Brendan Turrill', 'profile_path': None}, {'credit_id': '59ac0989925141072302bdfa', 'department': 'Art', 'gender': 2, 'id': 76497, 'job': 'Property Master', 'name': 'Brook Yeaton', 'profile_path': None}, {'credit_id': '59ac0a2cc3a3682c9c02add1', 'department': 'Sound', 'gender': 0, 'id': 1881596, 'job': 'Boom Operator', 'name': 'Matthew Armstrong', 'profile_path': None}, {'credit_id': '59ac0aa8925141072f02d282', 'department': 'Visual Effects', 'gender': 2, 'id': 1558086, 'job': 'Special Effects Supervisor', 'name': 'Matt Kutcher', 'profile_path': None}, {'credit_id': '59ac0b2ac3a3682c2202b192', 'department': 'Crew', 'gender': 2, 'id': 1558087, 'job': 'Special Effects Coordinator', 'name': 'Eric Roberts', 'profile_path': None}, {'credit_id': '59ac0b7ac3a3682c2202b1fb', 'department': 'Visual Effects', 'gender': 0, 'id': 1392098, 'job': 'Visual Effects Supervisor', 'name': 'Rocco Passionino', 'profile_path': None}, {'credit_id': '59ac0bbe925141077e02d0c4', 'department': 'Visual Effects', 'gender': 0, 'id': 1558716, 'job': 'Visual Effects Coordinator', 'name': 'Joseph Payo', 'profile_path': None}, {'credit_id': '59ac0bf2c3a3682cc802cefa', 'department': 'Visual Effects', 'gender': 0, 'id': 1408784, 'job': 'Visual Effects Producer', 'name': 'Chris Roff', 'profile_path': None}, {'credit_id': '59ac0c51c3a3682c48029d99', 'department': 'Lighting', 'gender': 0, 'id': 1881600, 'job': 'Best Boy Electric', 'name': 'Ulyan Atamanyuk', 'profile_path': None}, {'credit_id': '59ac0cbac3a3682c0a02cff6', 'department': 'Camera', 'gender': 0, 'id': 1881602, 'job': 'Key Grip', 'name': 'Chris Ekstrom', 'profile_path': None}, {'credit_id': '59ac0d54925141072f02d5e6', 'department': 'Lighting', 'gender': 0, 'id': 1484984, 'job': 'Best Boy Electric', 'name': 'Brad Garris', 'profile_path': None}, {'credit_id': '59ac0db0925141078a02df86', 'department': 'Camera', 'gender': 0, 'id': 1881603, 'job': 'Dolly Grip', 'name': 'Kendell Joseph', 'profile_path': None}, {'credit_id': '59ac0e5a925141077e02d39f', 'department': 'Camera', 'gender': 0, 'id': 1549179, 'job': 'Dolly Grip', 'name': 'Spencer Wilcox', 'profile_path': None}, {'credit_id': '59ac0e9f925141079d02bee6', 'department': 'Costume & Make-Up', 'gender': 0, 'id': 1552626, 'job': 'Key Costumer', 'name': 'Sarah P. Koeppe', 'profile_path': None}, {'credit_id': '59ac0ec1c3a3682bf0029524', 'department': 'Costume & Make-Up', 'gender': 0, 'id': 1881605, 'job': 'Seamstress', 'name': 'Catherine Rodi', 'profile_path': None}, {'credit_id': '59ac0eef925141070702c7ff', 'department': 'Costume & Make-Up', 'gender': 0, 'id': 1463801, 'job': 'Seamstress', 'name': 'Giselle Spence', 'profile_path': None}, {'credit_id': '59ac0f5dc3a3682c4802a0f5', 'department': 'Production', 'gender': 0, 'id': 1400837, 'job': 'Location Manager', 'name': 'John A. Johnston', 'profile_path': None}, {'credit_id': '59ac0ff2c3a3682c4802a196', 'department': 'Crew', 'gender': 0, 'id': 1844322, 'job': 'Production Controller', 'name': 'Gail Marks', 'profile_path': None}]	12314651
