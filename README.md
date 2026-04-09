Need a starting assumption about speed of drying. Then can apply Vapour Pressure Deficit to produce an assumed relation between T, RH and drying rate. 

Now let's apply VPD equation: 
https://en.wikipedia.org/wiki/Vapour-pressure_deficit

VPD = vp_sat * (1 - RH/100). [1]

https://en.wikipedia.org/wiki/Arden_Buck_equation 
vp_sat = 0.61121exp((18.678 - T/234.5)(T/(257.14+T))) (kPa) [2]

Let's assume that:
    - VPD has a linear relationship with drying time (https://www.researchgate.net/figure/Evaporation-rate-as-a-function-of-VPD-from-freshwater-and-saltwater-at-an-aeration-level_fig1_271421065)
    - at 20C, 70% RH, clothes take 2 hours to dry (https://www.reddit.com/r/explainlikeimfive/comments/1qobn49/eli5_what_are_the_weather_conditions_that_make/). This is the baseline. (Note that the time will also vary depending on the type of clothes being washed. Wind will also play a role. Clothes categories and wind can be included at a later stage.)

Let's add a drying time factor (F) such that F = 1 for the baseline. F=2 means that drying happens twice as slowly, and F=0.5 means that it happens twice as fast. Therefore F = VPD_0/VPD. [3]

And drying time, t = t_0 * F. [4]

From [1] and [2], VPD at the baseline = 0.70.

From [3] and [4], t = 2.0 * 0.70/VPD. [5] This is our drying time equation, that relates time to temperature and humidity. 

#TODO: tidy up README to clearly explain theory, provide clear user instructions, and list future work. 