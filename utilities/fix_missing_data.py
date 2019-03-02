def fixTrainRevenueAndBudget(df):
    # Populate missing revenue and budget numbers in the training set
    df.loc[df['id'] == 16,'revenue'] = 192864          # Skinning
    df.loc[df['id'] == 90,'budget'] = 30000000         # Sommersby          
    df.loc[df['id'] == 118,'budget'] = 60000000        # Wild Hogs
    df.loc[df['id'] == 149,'budget'] = 18000000        # Beethoven
    df.loc[df['id'] == 313,'revenue'] = 12000000       # The Cookout 
    df.loc[df['id'] == 451,'revenue'] = 12000000       # Chasing Liberty
    df.loc[df['id'] == 464,'budget'] = 20000000        # Parenthood
    df.loc[df['id'] == 470,'budget'] = 13000000        # The Karate Kid, Part II
    df.loc[df['id'] == 513,'budget'] = 930000          # From Prada to Nada
    df.loc[df['id'] == 797,'budget'] = 8000000         # Welcome to Dongmakgol
    df.loc[df['id'] == 819,'budget'] = 90000000        # Alvin and the Chipmunks: The Road Chip
    df.loc[df['id'] == 850,'budget'] = 90000000        # Modern Times
    df.loc[df['id'] == 1112,'budget'] = 7500000        # An Officer and a Gentleman
    df.loc[df['id'] == 1131,'budget'] = 4300000        # Smokey and the Bandit   
    df.loc[df['id'] == 1359,'budget'] = 10000000       # Stir Crazy 
    df.loc[df['id'] == 1542,'budget'] = 1              # All at Once
    df.loc[df['id'] == 1542,'budget'] = 15800000       # Crocodile Dundee II
    df.loc[df['id'] == 1571,'budget'] = 4000000        # Lady and the Tramp
    df.loc[df['id'] == 1714,'budget'] = 46000000       # The Recruit
    df.loc[df['id'] == 1721,'budget'] = 17500000       # Cocoon
    df.loc[df['id'] == 1865,'revenue'] = 25000000      # Scooby-Doo 2: Monsters Unleashed
    df.loc[df['id'] == 2268,'budget'] = 17500000       # Madea Goes to Jail budget
    df.loc[df['id'] == 2491,'revenue'] = 6800000       # Never Talk to Strangers
    df.loc[df['id'] == 2602,'budget'] = 31000000       # Mr. Holland's Opus
    df.loc[df['id'] == 2612,'budget'] = 15000000       # Field of Dreams
    df.loc[df['id'] == 2696,'budget'] = 10000000       # Nurse 3-D
    df.loc[df['id'] == 2801,'budget'] = 10000000       # Fracture
    
    return df
    
def fixTestRevenueAndBudget(df):
    # Populate missing revenue and budget numbers in the test set
    df.loc[df['id'] == 3889,'budget'] = 15000000       # Colossal
    df.loc[df['id'] == 6733,'budget'] = 5000000        # The Big Sick
    df.loc[df['id'] == 3197,'budget'] = 8000000        # High-Rise
    df.loc[df['id'] == 6683,'budget'] = 50000000       # The Pink Panther 2
    df.loc[df['id'] == 5704,'budget'] = 4300000        # French Connection II
    df.loc[df['id'] == 6109,'budget'] = 281756         # Dogtooth
    df.loc[df['id'] == 7242,'budget'] = 10000000       # Addams Family Values
    df.loc[df['id'] == 7021,'budget'] = 17540562       #  Two Is a Family
    df.loc[df['id'] == 5591,'budget'] = 4000000        # The Orphanage
    df.loc[df['id'] == 4282,'budget'] = 20000000       # Big Top Pee-wee
    
    return df
    
def fixTrainRuntime(df):
    # Populate missing runtime values in the training set
    df.loc[df['id'] == 391, 'runtime'] = 86 #Il peor natagle de la meva vida
    df.loc[df['id'] == 592, 'runtime'] = 90 #А поутру они проснулись
    df.loc[df['id'] == 925, 'runtime'] = 95 #¿Quién mató a Bambi?
    df.loc[df['id'] == 978, 'runtime'] = 93 #La peggior settimana della mia vita
    df.loc[df['id'] == 1256, 'runtime'] = 92 #Cipolla Colt
    df.loc[df['id'] == 1542, 'runtime'] = 93 #Все и сразу
    df.loc[df['id'] == 1875, 'runtime'] = 86 #Vermist
    df.loc[df['id'] == 2151, 'runtime'] = 108 #Mechenosets
    df.loc[df['id'] == 2499, 'runtime'] = 108 #Na Igre 2. Novyy Uroven
    df.loc[df['id'] == 2646, 'runtime'] = 98 #同桌的妳
    df.loc[df['id'] == 2786, 'runtime'] = 111 #Revelation
    df.loc[df['id'] == 2866, 'runtime'] = 96 #Tutto tutto niente niente
    
    return df
    
def fixTestRuntime(df):
    # Populate missing runtime values in the testing set
    df.loc[df['id'] == 4074, 'runtime'] = 103 #Shikshanachya Aaicha Gho
    df.loc[df['id'] == 4222, 'runtime'] = 93 #Street Knight
    df.loc[df['id'] == 4431, 'runtime'] = 100 #Плюс один
    df.loc[df['id'] == 5520, 'runtime'] = 86 #Glukhar v kino
    df.loc[df['id'] == 5845, 'runtime'] = 83 #Frau Müller muss weg!
    df.loc[df['id'] == 5849, 'runtime'] = 140 #Shabd
    df.loc[df['id'] == 6210, 'runtime'] = 104 #Le dernier souffle
    df.loc[df['id'] == 6804, 'runtime'] = 145 #Chaahat Ek Nasha..
    df.loc[df['id'] == 7321, 'runtime'] = 87 #El truco del manco
    
    return df
    
def fixLowDollars(df):
    # Some films are showing number like 1.5 for 1500000 so convert those
    # Find films with a budget larger than 1000 with revenue less than 100
    tomod = df.id[df.budget > 1000][df.revenue < 100]
    
    # For the identified films multiply the revenue by 1,000,000
    for x in tomod:
        df.loc[df['id'] == x, 'revenue'] = df.loc[df['id'] == x, 'revenue'] * 1000000
        
    return df