# 2021Fall_finals

Team Members:

1. Sahit Potnuru (potnuru3), GitHub: sahit10
2. Vanika Gupta (vanikag2), GitHub: VanikaGupta95

## Team Members:
1.	Sahit Potnuru (potnuru3), GitHub: sahit10
2.	Vanika Gupta (vanikag2), GitHub: VanikaGupta95
## Effectiveness of background checks on crime rates in US
Background checks for gun purchases are designed to prevent access to guns by convicted felons and other prohibited possessors. About 1 in 5 gun transactions in the U.S. occur without a background check, according to a 2017 study by researchers at Harvard and North-eastern University.

Though more than 90% of the American public supports background checks for all gun sales, a dangerous and deadly loophole in federal gun laws still exempts unlicensed sellers from having to perform any background check whatsoever before selling a firearm. With this loophole, guns easily find their way into the hands of illegal buyers and gun traffickers, dramatically increasing the likelihood of gun homicides and violent crimes.

Universal background check may reduce gun-related homicides or violent crimes by deterring prohibited possessors from attempting to acquire firearms or by making it harder or more expensive for them to succeed in doing so.

## Project Goal:
Crime rates are proportional to the firearm background checks processed through the National Instant Criminal Background Check System (NICS). It is necessary that background checks must be conducted before possessing a firearm. We have considered five data sets:

•	[NICS firearm background checks from 1998 to 2021](https://github.com/Sahit10/2021Fall_finals/blob/main/Firearm_homicides.csv)

•	[Crimes committed by adults in the age group 18 to 65 years from 1994 till 2016.](https://github.com/Sahit10/2021Fall_finals/blob/main/arrests_national_adults.csv)

•	[Crimes committed by juveniles in the age group 0 to 17 years 1994 till 2016.](https://github.com/Sahit10/2021Fall_finals/blob/main/arrests_national_juvinile.csv)

•	[Total firearm homicide incidents from 2014 till 2020.](https://github.com/Sahit10/2021Fall_finals/blob/main/Firearm_homicides.csv)

•	Violent crime incidents from 1998 to 2020 - API 

Based on the above datasets we will be analysing the conclusions stated in the research papers mentioned in References. Following are the conclusions.

#### Conclusion 1: Effect of background checks on violent crimes is inconclusive. 

#### Conclusion 2: Dealer Background checks may reduce firearm homicides and private-seller background checks on firearm homicides is inconclusive.

Six studies examined the overall effect of dealer background checks on firearm homicide rates: Two used large independent data sets and found significant effects indicating that dealer background checks reduce firearm homicides

One analysis found significant effects consistent with private-seller checks increasing firearm homicides, although these estimates became uncertain or significant in the opposite direction in different specifications. Another study found suggestive effects consistent with private-seller checks increasing firearm intimate partner homicides.


## Conclusion:
As seen below the Total Background Checks and Total Dealer Checks conducted each year from 1998 till 2021 increases sharply from 1998 till 1999. After which there is a gradual increase in both the checks with minor fluctuations till 2020 and then there is a steep decline in the checks conducted. One reason can be Covid-19 pandemic which hit the world in 2020 thus reducing the total checks conducted post 2020.

![](Images/Background_checks_trend.png)

Below is a bar plot that shows state wise total number of background checks. As seen, the maximum number of checks are administered in the state of Kentucky and least being in the Mariana Islands where population resides on Saipan, Tinian, and Rota. 

![](Images/Background_checks_states.png)

Critiquing on the Conclusions from the research papers as stated above:
#### Conclusion 1: Effect of background checks on violent crimes is inconclusive.

![](Images/Violent_crimes_bchecks.png)

As highlighted, it is clearly seen that the value of correlation coefficient is -0.89 for total checks vs total crimes for the period 1998 till 2020. There is a high negative correlation between these two variables, hence an increase in the total background checks decreases total violent crimes. 


Now only considering California, Colorado, Delaware, Maryland, Nevada, New Jersey, New York, Oregon, Vermont, and Washington where background checks are mandatory. Firearm transfers are conducted by or processed through licensed dealers, who conduct background checks on prospective firearm purchasers or recipients.
Looking at the correlation plot for the filtered states:

![](Images/Bchecks_violent_Filtered_states_crimes.png)

The value of correlation coefficient for total dealer checks and total background checks vs crimes is -0.86 indicating a high negative correlation between the mentioned two variables. Hence, we can conclude that an Increase in the background checks will decrease the rate of violent crimes.
Based on our analysis we can clearly deduce that an increase background check will decrease the rate of violent crimes and hence the results are not inconclusive. 


#### Conclusion 2: Dealer Background checks may reduce firearm homicides and private-seller background checks on firearm homicides is inconclusive.

Dealer background checks are slightly negatively corelated with total number of homicides, Private seller background checks are slighlty positively correlated with total number of homicides also Total Checks are almost showing very less to no correlation with homicides as seen below:

 ![](Images/Bchecks_Firearm_homicides.png)


## Future Scope and Analysis:

We have further analysed the following:

•	Effectiveness of background checks on violent crimes and homicides based on ethnicity i.e., for White, Black, Pacific Asian, and American Indian. 
  
 ![](Images/Adult_homicide.png)
 
 ![](Images/adult_violent_crime.png)
 
 ![](Images/Juvi_homicide.png)
 
 ![](Images/Juvi_violent_crimes.png)
 
 ![](Images/Adult_Juvi_Homicides.png)
 
 ![](Images/Adult_Juvi_Violent_Crime.png)
  


## Limitations:
1. Time frames of the events taken into consideration are different across different cross sections.
2. The type of crimes taken into consideration are different across different studies.
3. Different states have different kinds of rules to handle gun violence so cummulative study might have impact due to the difference in rules.

## References:
1.	https://www.rand.org/research/gun-policy/analysis/background-checks.html#fn2
2.	https://wamu.org/story/20/06/25/do-universal-background-checks-prevent-gun-violence/
3.	https://www.rand.org/research/gun-policy/analysis/background-checks/violent-crime.html
4.	https://www.rand.org/research/gun-policy/analysis.html
5.	https://giffords.org/lawcenter/gun-laws/policy-areas/background-checks/universal-background-
6.	https://www.gunviolencearchive.org/last-72-hours
7.	https://medium.com/@szabo.bibor/how-to-create-a-seaborn-correlation-heatmap-in-python-834c0686b88e



