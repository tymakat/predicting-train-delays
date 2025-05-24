This is for catching up when I come back to the project after a (long) break

Sort of a whitepage

# Idea

Create a website that boosts my portfolio, showing off both my skills as an API Developer and a Data Scientist, allowing to apply to more jobs, showcasing my work value. This will enrich my portfolio in the end.

Specifically - train a model to predict Departure delay (MVP), total trip delay (MVP+) and cancellation certainty (MVP++)

## Workflow:

Website let's the user select the departure/arrival time -> User sees different trip options, fetched from NS API -> User selects a trip: using NS API, things like station, platform changes and everything else are fetched -> User sees the arrival delay estimate for their trip, user can click refresh button, which re-fetches the info from NS. 

The fetched data is fed to a model that then makes a prediction on a delay

## Work validation

To make the person see that the model works as intended:

a) Upload the model and the notebook to github, showing how to run predictions against the dataset to test it themselves
b) Flashy accuracy metrics, recall matrixes, r-square values, etc.
c) Make a "live-predictions tab" that allows a user to see the predictions model makes in real time, and later check in on this predictions to validate if they were true or not
d) Make a tab with "Saved trips" or something like this, which lets user see their trips, predicted and actual delay time.

## Dataset observations

- The delay is always 0, if arrival cancelled = true or departure cancelled = true

- Amount of departures cancelled equals the amount of arrivals cancelled

- No journeys with one stop

- Arrival delay always = 0 if It's first station
- Departure delay always = 0 if it's last station

- In wast majority of cases (99.7%, arrival delay = Null on first station; departure delay = Null on last station)
- Delay breakdown: 66% no delay at all, 19% 1-2 minutes, 5% - train was cancelled, 6%: 3-5 minutes, 3% the rest.

## Limitations

1) Computing power - might need to train the model on the cloud
2) API calls - only 300 calls per day, not that much, might need to text NS

### Progress so far:

1) Started preprocessing the dataset, removed basic shit, limited to just NS and Intercity + Sprinter
2) Analyzed the dataset to avoid being paranoid that it doesn't work properly, found some interesting things

### Definition of an MVP

#### Absolute MVP (build no matter what)
- Live fetching of data using NS API
- Pages allow the user to select the trips, and choose the option for navigation, random number is being spat out by the model
- Simple one page design: Enter time, date, select the train, see estimated delay
- Model doesn't even have to work
- No live updates pages, no "proof of work" by the model, no github setup repo
- No cancellation estimate

#### Normal MVP (fallback if model can't adequately predict delay precisely)

- All mentioned previously plus:
- User can view their journeys in a separate window
- Model works, but only predicts departure delay, and only predicts if the train will be delayed or not (Nothing more than that)
- Confustion matrix provided
- Still no live updates
- No github repo

### MVP Plus (Normal product)

- Model predicts total delay for the journey (model predicts arrival and departure delay for every leg, and then it get's aggregated)
- Model predicts delay in range (0-1 minutes, 2-3, 2-4, etc)
- Still no cancellation
- This is already good enough to start flexing the model in Data Science projects, create github repo
- Popular delay destinations suggested to user on the home page

## MVP Plus Plus (Extra)

- Added cancellation prediction
- Nice icons and animations of trains
- Live delay estimates (figure out how to bypass the limit of 300 request per day)



### Design: Model
This part contains the explanation on how to train the model

1) Data sourcing
2) Data cleaning
3) Data preprocessing
4) Model picking
5) Additional preprocessing
6) Feature selection
7) Additional preprocessing/finetuning
8) Comparing models results
9) Selecting model that performs best
10) Fine-tuning 
11) Success

Data sourcing

I have open source data from NS, enough for now.

Restrictions:

If the data is not in the API (we can't get this data immediately), the feature is excluded

Features one by one:

Main dataset

RDT-ID:
Obsolete

Date
Remove, there's departure and arrival time features
- Arrival/departure date null? Remove entry
- Arrival/departure date in an incorrect format? Standardize
- 

Type:
Keep, but I think it vaguely correlates

Company:
Remove, we only keep NS for simplicity

Completely cancelled/partly cancelled: 
remove for delays, potentially keep as target features for cancellation prediction (beyond the scope for now)

Train number:
Keep, but I think it correlates even more vaguely than train type

Maximum delay:
Remove, just represents maximum delay for the journey, the delay must be compound instead 

Encoding stations into numerical format:
Approach 1 - consider that the parameters like busyness, route distance and size, etc. are already encoded in the station

Convert the journey (arrival/departure city pair) to a unique number, perform prediction on that number

Approach 2 - extract as much meaningful features as possible - busyness, station size, route distance, etc.

(Question - is it worth it extracting more features?)

1) Preprocess to include maintenances AND other disruptions
In the format - maintenance - True/False and disruption - True/False
2) Reformat all rows to journeys: departure station and arrival station
3) Add new feature - total delay. It's a compound of arrival delay for arrival station and departure delay for departure station. (already there, just make sure delays are compounded correctly)
4) Add new feature - is peak hours (already there by me)
5) Add new feature - is holiday/weekday/weekend
6) Calculate if there was a platform change for arrival station


Treat Null values in Arrival cancelled/Departure cancelled as Falses
Remove "Arrival/Departure" partially cancelled

Dataset observations:
If the departure or arrival cancelled = True, the delay will be 0

Remove all entries with arrival/departure cancelled = true. Cancellation training will be done separately.

Amount of departures cancelled equals the amount of arrivals cancelled

Are there journeys with only one stop? No

Arrival delay always = 0 if It's first station
Departure delay always = 0 if it's last station

