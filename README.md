# 2021Fall_finals

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

<img src=Images/Background_checks_states.png width="17000" height="500">

Critiquing on the Conclusions from the research papers as stated above:
#### Conclusion 1: Effect of background checks on violent crimes is inconclusive.

<img src=Images/Violent_crimes_bchecks.png width="800" height="600">

As highlighted, it is clearly seen that the value of correlation coefficient is -0.89 for total checks vs total crimes for the period 1998 till 2020. There is a high negative correlation between these two variables, hence an increase in the total background checks decreases total violent crimes. 


Now only considering California, Colorado, Delaware, Maryland, Nevada, New Jersey, New York, Oregon, Vermont, and Washington where background checks are mandatory. Firearm transfers are conducted by or processed through licensed dealers, who conduct background checks on prospective firearm purchasers or recipients.
Looking at the correlation plot for the filtered states:

<img src=Images/Bchecks_violent_Filtered_states_crimes.png width="800" height="600">

The value of correlation coefficient for total dealer checks and total background checks vs crimes is -0.86 indicating a high negative correlation between the mentioned two variables. Hence, we can conclude that an Increase in the background checks will decrease the rate of violent crimes.
Based on our analysis we can clearly deduce that an increase background check will decrease the rate of violent crimes and hence the results are not inconclusive. 


#### Conclusion 2: Dealer Background checks may reduce firearm homicides and private-seller background checks on firearm homicides is inconclusive.

To understand the effect of Dealer Background checks and Private Seller checks on firearm homicides, let us refer the below graph: 

 ![](Images/Bchecks_Firearm_homicides.png)

The coefficient of correlation is -0.35 for total dealer checks and total number of homicides. Hence, these two variables are slightly negatively correlated indicating that an increase in the dealer checks will slightly reduce the total homicide incidents. 

Moving on to the total private checks, the coefficient of correlation is 0.3. This shows a slight positive correlation between total private checks and total homicides. Hence, we can deduce that an increase in the private seller background checks will increase homicide incidents. 

The overall background checks have a coefficient of correlation -0.14 suggesting very less correlation will total homicides. 

Based on our analysis we can conclude that an increase in the dealer checks may moderately reduce the total homicide incidents whereas an increase in the private seller background checks may moderately increase homicide incidents. 


## Future Scope and Analysis:
Further analysing Adults and Juveniles crime data for total arrests which is the cumulative of arrests for each ethnicity i.e., for White, Black, Pacific Asian, and American Indian against the total background checks conducted from 1998 till 2016.

#### •	Arrests of adults for violent crimes:



Only considering adults first, the coefficient of correlation for total checks vs total violent crime arrests for adults is -0.6. This signifies they are negatively correlated indicating that if background checks are increased for adults, the total arrests for violent crimes may decrease. 

#### •	Arrests of adults for homicides:



The coefficient of correlation for total checks vs total homicide arrests for adults is -0.79 This signifies they are highly negatively correlated indicating that if background checks are increased for adults, the total arrests for homicides will decrease. 

####  •	Arrests of juveniles for violent crimes:



Now considering juveniles, the coefficient of correlation for total checks vs total violent crime arrests for juveniles is -0.93. This signifies they are significantly negatively correlated indicating that if background checks are increased for juveniles, the total arrests for violent crimes will decrease. 

#### •	Arrests of juveniles for homicides:



The coefficient of correlation for total checks vs total homicide arrests for juveniles is -0.86. This signifies they are highly negatively correlated indicating that if background checks are increased for juveniles, the total arrests for homicides will decrease. 

#### •	Arrests of adults and juveniles for violent crimes based on ethnicity:



As seen in the plot above, the coefficient of correlation for total checks vs total arrests for adults and juveniles is -0.93. This signifies they are highly negatively correlated indicating that if background checks are increased for adults and juveniles, the total arrests for violent crimes will significantly decrease. 

##### Ethnicity wise analysis:

Race            | Coefficient of Correlation | Interpretation
----------------| ---------------------------| --------------------------------
White           | -0.95                      | Significant negative correlation
Black           | -0.82                      | Significant negative correlation
Pacific Asian   | -0.94                      | Significant negative correlation
American Indian | -0.88                      | Significant negative correlation

As there is a significant negative correlation between total background checks and total arrests for all the ethnicities, we can clearly infer that an increase in the background checks will significantly decrease the violent crimes for adults and juveniles. 


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



