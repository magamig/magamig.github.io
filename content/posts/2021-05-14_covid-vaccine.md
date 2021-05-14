---
title: "Scraping for a COVID-19 Vaccine"
date: 2021-05-14T15:00:00+01:00
location: "France"
---

<div class="info">

ℹ️ **COVID-19 vaccine**<br/>
Learn more from the [World Health Organization](https://www.who.int/emergencies/diseases/novel-coronavirus-2019/covid-19-vaccines).

</div>

Earlier today, I went to get my first COVID-19 vaccine dose. Although accross the pond it might seem normal for a young person to be getting the vaccine, it's still considered early for continental Europe, in particular France. So how did I get mine?

Firstly, I'd like to make it clear that I did not cut in line! The elderly population, health care and other essential workers, or those clinically vulnurable are already vaccinated by now (or have access to a priority queue). Currently, the French goverment is vaccinating by phases using the age as the only criteria, but sometimes people change or cancel their appointments. When these gaps are not filled by the eve of the appoitnment **and** the vaccine is tempperature sensitive, these slots are up for grabs for the non-priority population. The reasoning behind this is that it is better to have someone non-prioritary taking the vaccine, than letting it go to waste. Which is true for the Pfizer-BioNTech and Moderna vaccines. [^1]

[^1]: Crommelin, D. J., Anchordoquy, T. J., Volkin, D. B., Jiskoot, W., & Mastrobattista, E. (2021). Addressing the cold reality of mRNA vaccine stability. Journal of Pharmaceutical Sciences, 110(3), 997-1001.

In order to make an appoitment, you had to visit [doctolib.fr](https://www.doctolib.fr/) and search for a vaccination center near you with a vacant time for that same day or day after. However, finding a slot was near to impossible, since it only happened when people cancelled their appointment at the last minute. You could try your luck constantly reloading the page until you got lucky, but there had to be a better way!

When selecting the type of vaccine, I noticed it would send a `GET` request to the server that would receive the dates you sent with the available slots for those days and **the next available slot**. It should be clear where this is going from now on.

![](/image/schedule_vaccine_covid.png)

Within a couple of minutes, I had a fully working **`Python` script that** asked the server every 10 seconds when was the next slot available, until it found a vacancy. Afterwards, it would open the booking website, where I would manually fill out the form. I left it running shy of 2 hours, until **I successfully got my apointment for today!** 

<pre>
import sys
import time
import webbrowser
import requests
import datetime

found = False
while not found:
    today = datetime.datetime.today()
    try:
        r = requests.get(url = API_URL)
        data = r.json()
        next_slot = datetime.datetime.strptime(data['next_slot'], '%Y-%m-%d')
        print(f'Next slot: {next_slot}')
        if((next_slot - today).days < 1):
            webbrowser.open(URL)
            found = True
        else:
            time.sleep(10)
    except KeyError:
        continue
</pre>
