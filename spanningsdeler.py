# 0 - 1023
# 
# 9V - 12V
# 
#  / 4 = 2,25V - 3V

#  die range wordt gemapped als 0 tot 5 volts naar 0 - 1023 NIET ALS JE DE RESOLUTIE OMHOOG GOOIT BOEM!! 0 - 65535

#  5/65535

#  die range 2,25V - 3V wordt dus 29.490,75 tot 39.321 (hoewel de max niet helemaal de max is want de accu kan wellicht boven de 12V komen)

# dus gewoon map de analogread van de arduino (als we de resolutie omhoog gooien) naar 0 - 100

# map(analogread(pinding), 29.490,75, 39.321, 0, 100)    OF      map(analogread(pinding), 29.490,75, 39.321, 9V, 12V)

# de nano ondersteunt geen hogere resoluties, dus de range is toch 460,35 tot 613,8

# dus map(analogread(pinding), 461, 614, 0, 100)