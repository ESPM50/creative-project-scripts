# https://docs.google.com/spreadsheets/d/1P4p-H_lgakBGMWgpgYMGh696gwPBjjfVTyd2USY16Og/edit#gid=139929664
data = [
    ('442nd Regimental Combat Team', 'Johnson, Madeleine ', 'family searching for the american dream,ww2,442nd regimental combat team'),
    ('Acculturation of Chinese Immigrants in San Francisco', 'Wang, Alex;Wu, Guang', 'assimilation,acculturation,chinese immigrants,immigration,chinese-american'),
    ('An Ecosystem\'s Intervention for Pesky People', 'Nussbaum, Jasper;Schiff, Anna', 'human impact,socal mediterranean ecosystem,children\'s book,decline in environmental integrity,extent of human culpability,possible restorative actions'),
    ('Animal Agriculture', 'Carabuena, Sara Kate', 'animal agriculture,environmental impact,climate change'),
    ('Colonization in the Northeast', 'Montanez, Martha', 'fur trade,introduction to catholicism,trading among northeastern tribes'),
    ('Commodification of Nature in a Changing Environment', 'Naik, Nishali', 'natural resources,big business,pollution'),
    ('Images ', 'Mallit, Ben', 'asian american immigrants,ecology and california marine biology,worster\'s analytical framework'),
    ('Continuities and Change over time in the Social and Political Attitudes towards the Chinese over the 19th to 20th centuries', 'Huang, Angela', 'federal policies/social reactions,labor,immigration,'),
    ('Contrasting Realities ', 'Erin , Cain ', 'environmental justice,ecosystems,exploitation'),
    ('Deer to Me', 'Jung, Catherine', 'natural resources,assimilation and acculturation,family history'),
    ('Eastern Sunset', 'Hwang, Anna;Won, Jeanie;Wong, Eric', 'chinese immigration,eastern and western agriculture,cultural differences,agriculture,california,immigration'),
    ('Environmental Effects of the Meat Industry ', 'Wood, Melissa', 'meat industry,environmental pollution,methane emission'),
    ('Environmentally Mindful', 'Johnson, Marisa', 'environmental education,sustainability,propaganda'),
    ('Film Series: Water in California', 'Sanchez Alcaraz, Andy', 'water resource management,water drought ca,water use'),
    ('Four Pieces on Nature', 'Chen, Fei', 'music,fire usage,katrina'),
    ('Issei', 'Jow, Owen', 'japanese cultural identity,property rights,nursery industry'),
    ('leave only footprints', 'Pearson, Kate', 'human impact on environment,natural/manmade material,interaction/performance with nature'),
    ('Modeling the Path to Disaster', 'Kim, Yoona;Suresh, Sahana;Tang, Sarah', 'racially differentiated risk,hurricane katrina,landscape in new orleans,la'),
    ('Natural skin care ', 'Ajayi, Iyioluwa;Nguyen, Vy ', 'skin care products,healthcare,environment,beauty'),
    ('Nature and Civilization Collide ', 'Anderson , Julia ', 'california topography,erosion,manmade structures'),
    ('Net-Zero Application', 'Acuna, Michelle', 'affordable housing,environmental justice,green architecture'),
    ('Oxford Tract Resistance', 'Hernandez, Lauren;White, Angela ', 'student activism,community engagement,environmental education'),
    ('Personal history of Chinese American women ', 'zhan, shuya', 'chinese immigration,resistance,women\'s role'),
    ('Pesticides', 'Li, Jeffrey;Le, Sabrina;Zhong, Justin', 'naled,ddt,methyl bromine,methyl bromide'),
    ('Project Short Story', 'Fann, Amy;Chu, Brenton', 'bp oil spill,identity,preservation of natural resources,environmental preservation'),
    ('Ceiling to the Sand', 'Campos, Josh', 'systemic poverty,resource management,power'),
    ('Sketch series on the Ohlone People\'s natural resource use and interaction', 'Wagner, Emily', 'ohlone,natural resources,interaction with nature'),
    ('The Chinese Immigrant Story', 'Lin, Helen;Thai, Thanh Thanh. ', 'chinese immigrant experience,california gold rush,transcontinental railroad'),
    ('The conflict of man and nature', 'Turnbull, Chase', 'man and nature,nature as sacred,nature as a resource'),
    ('the ecological Indian and his land ', 'Babikian, Karnie', 'woodland indians pre contact,cultural appreciation,niche in nature/land'),
    ('The Faces of Hurricane Katrina', 'Mateo, Crystal', 'hurricane katrina,individual impact,environmental racism'),
    ('The Gold Rush', 'Kim, Ashley', 'gold rush,mining,immigrants'),
    ('Hey, CAreful with that WATER', 'Wu, Lisa', 'change in landscape and land use in california'),
    ('Transition of American Views on Natural Resources', 'Kim, Heidi;Li, Amy', 'views of nature,native americans,europeans'),
]

data = [
    dict(zip([ 'title', 'authors', 'tags' ], row))
    for row in data
]
