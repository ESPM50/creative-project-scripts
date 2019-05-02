# https://docs.google.com/spreadsheets/d/1P4p-H_lgakBGMWgpgYMGh696gwPBjjfVTyd2USY16Og/edit#gid=139929664
data = [
    ('A Brief Visual History of San Francisco ', 'Morales, Daniela', 'culture and enviroment,maps,san francisco golden gate', '57524447421'),
    ('After (Im)possibilities: A Remix of History/Sameness', 'Harcourt, Rebecca;Shin, Yuju', 'culture,expansion,society,nature,environment', '57525074384'),
    ('Artistic Rendition of a Changing Landscape', 'Valdez, Madeleine', 'environmental history,urban development,bay area', '57524978420'),
    ('Changing landscape in the New World due to colonization', 'Kim, Laura;Patel, Kishan;Quin, John', 'colonization,change,nature,californian indian displacement', '57525052768'),
    ('Food and Footprints', 'Kim, Allison;Yeo, Ji Hun', 'carbon footprint,food,sustainability,personal impact,different diets,greenhouse gases,environmental sustainability', '57524402082'),
    ('Instrument and Sublime', 'Lee, Christian', 'chinese laborers,transcontinental railroad,exclusion from americanization and american history', '57524455169'),
    ('Water in California', 'Wu, Yi-Chi', 'water,development and exploitation,landscape change', '57524466275'),
    ('[Untitled: interaction of Chinese immigrants and North American natural resources]', 'Cho, JoAnn; Lau, Whitney', 'chinese laborers, natural reousrces, chinese, railroad', '')
] # last item in tuple (box_id) discarded.
data = [
    dict(zip([ 'title', 'authors', 'tags' ], row))
    for row in data
]
