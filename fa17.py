import tempfile
import os

from functional import seq
from boxsdk import DevelopmentClient

from zotero import *
from img_extract import extract_from_pdf, extract_from_docx, extract_all
import box
import similarity

BOX_URL_PREFIX = 'https://berkeley.app.box.com/folder/'
BOX_INPUT_FOLDER = '57392956412' # A&E FOLDER ONLY

COLLECTION_NAME = 'fa17_0'
SEMESTER_TAG = 'fa17'

# https://docs.google.com/spreadsheets/d/1NjsPhr4jrShfovbauydKbYvE77kLrVZorN-J7QJ0vRU/edit#gid=306034460
data = [
    ('Hubris', 'Luc , Anna ', 'My artwork is referring to Hurricane Katrina. I wanted to convey the message that the consequence of Hurricane Katrina were amplified by factors that could have been prevented if we practiced a more holistic and responsible approach in dealing with natural disasters . ', '2 pieces of 6x9x.03', 'Oil Paint, Canvas, Markers.'),
    ('Looking to the Future from the Past - The California Condor', 'Abranches Da Silva, Matthew', 'The mixed media piece depicts the human factors which contributed to the extinction in the wild of the California Condor. From the bullet shards in the nest and the DDT bottle in the cave to the gold on the mountains and chains surrounding the bird, the piece is full of symbolism. "Looking to the future" is in the title of the piece because the purpose is not to dwell on  past problems, but rather to get people thinking about how the past will influence the California condor species, now that it has been reintroduced into the wild.', '24" x 24"', 'Mixed Media- primarily acrylic paint, with the use of metal chains, cage wire, aluminum, and gold foil'),
    ('[untitled sculpture of Hawaii]', 'Nicholson, Metta', 'This piece portrays the interconnectedness of human societies and coral ecosystems, as well as the consequences that arise with the issue of coral bleaching. The clay island represents Hawaii, a part of the United States that has felt the impacts of coral bleaching; this island is supported by human hands, revealing the role that humans must play in preserving the integrity of the environment around them. The white clay figures on the blue background represent bleached coral in an ecosystem that has suffered from dwindling biodiversity. The goal of this piece is to stress the importance of healthy coral reefs to maintaining the livelihood of our coastal communities.', '12 x 9 x 2 (inches)', 'Acrylic paints were used to paint the canvas. The island, coral, and parts of the ocean were crafted from clay.'),
    ('Japanese Americans and the Environment during Internment', 'Kishi, Alyson', 'My grandparents were interned during World War II at Poston and Heart Mountain, so this was a very personal and informative experience for me.  I talked to my grandma about creating these pieces, so I hope that the art conveys her memories and her feelings about internment.  I wanted to focus on how the harsh, barren environment was both a form of oppression but also a tool for resistance and survival.  Despite their grim circumstances and forced removal, Japanese Americans were resilient and found a sense of purpose by transforming the landscape, whether by farming, planting gardens, digging canals, or exploring the outdoors.  I used very muted and faded out watercolor to parallel the Japanese American\'s removed and oppressed lives in camp alongside bolder colors to symbolically represent the prisoners\' spirit and perseverance.', 'Three 9"x12" paintings', 'Watercolor'),
    ('The more we place importance on greed, the less future we have', 'Amick, Joanna', 'The recent proposal to repeal the Clean Power Plan was the inspiration for this muralesque painting. With the repeal, it is extremely likely there will be an increase in the CO2 emissions as regulations will be minimized, promoting continued use of coal power plants. While California is making its own clean power regulations, the CO2 emissions increasing in the future for the majority of the United States will still have effects in California. Not only does the increase in air pollution cause health issues as well as expedite aging, the continuing decline of snow in the California Sierra Nevada mountains will also minimize the water resources in California.', '18 inches x 24 inches x 2 inches', 'acrylic paint and glazes on canvas'),
    ('From the Fire', 'Gallo, Annie', 'In the wake of the October fires that devastated my community in the North Bay, I wanted to create a piece that symbolized hope and rebirth in a time of tragedy. I drew upon readings from my ESPM 50 class that recalled the fire management techniques that Native Americans used; we learned how their fires revitalized the soil with essential nutrients and eventually created lush meadows. I can only hope that the same spirit of rejuvenation will make the North Bay even stronger in the tough years to come, as people try to reassemble their lives after the most devastating urban wildfire California has ever seen. ', '16" x 20" x 1.5"', 'Acrylic on canvas, ash found on Route 12 near Glen Ellen'),
    ('Generations', 'Lee, Fionna;Yuki, Cameron; Nguyen, Tiffany', 'Our project focuses on the contrasting serendipities of time and unfortunate hardships that shaped the Japanese immigrant experience, from their entrance into the agricultural sector starting 1884, through Japanese internment during World War 2, to their present-day experience in California. The painted backdrop reflects their emotional circumstances throughout this reverse timeline of Japanese generations. We incorporated mixed media as symbolic imagery of their culture with emphasis on Japanese impacts on the environment. ', '16" x 12" x 1" ', 'canvas, paint, mixed media: paper, dirt, plants, wire, glue, coffee, plastic'),
    ('Station Aloha', 'Romulo, Katrina;Winner, Sam', 'Ocean acidification is the process in which high concentrations of atmospheric carbon dioxide are deposited into oceans, altering the water\'s chemical makeup. Carbonic acid, free hydrogen ions, and bicarbonate molecules are direct byproducts which offset and degrade the health of ocean climates. Second degree effects include increased water temperatures, calcification impedance, and coral degradation. While these are universal products, they significantly affect coastal cities such as Honolulu, which heavily depend on marine habitats for economic, social, and environmental stability. Each art piece accompanies a concept associated with ocean acidification and perpetuates the notion that awareness and action must be generated - Hope you enjoy! ', '22 x 36 x 0', 'Photoshop and illustrator on paper '),
    ('[untitled 4 shirts]', 'French, Arran', 'I am creating four shirts inspired by the four respective units in the class. The first exemplifies the unjust disaster of Katrina, the second draws upon the divergent myths of the Native Americans and colonists, the third calls attention to the Chinese immigrants role in building the Union Pacific Railroad, and the fourth highlights the major issues with California’s water management system.', '4 buttondown shirts', 'Cotton fabric'),
    ('Into the Ditch: Fleeing a Third World', 'Sengchanthavong, Dara', 'My mother was a child refugee during the Viet Nam War; as her family escaped Laos and headed into Thailand, her father yelled, “Quick, into the ditch!” to avoid the bombs the United States released onto our motherland. The trauma of fleeing war has left my mother in a state of displacement, making navigating life in America difficult. Many Southeast Asian communities are still trying to assimilate to a country that does not want them, a country that does not welcome refugees. Even now, many Southeast Asian communities still live in poverty and face environmental injustices—like food insecurity and poor living conditions—because the US Government fails to acknowledge and aid the communities it pushed out of their own motherland. At the center is the ditch my mother would curl up in to avoid the bombs, but it still resides within her and passed down unto her children where we remain in the ditch and are continuing the struggle of getting out.', 'Panels of 6x8 in. Pieces (Subject to change based on arrangement)', 'Watercolor, Ink, & Acrylic on Paper'),
    ('Chasing the Beavers', 'Jiang, Jia;Dai, Xiaoyu; Chen, Peiying', 'This drawing focus on the environmental changes due to the vast hunting of beavers during the fur trade period. The goal is to inform that any actions we take right now will affect not only human, but the whole ecosystem around us.\n\nThis time we choose to do a drawing to show our topic on the impact of the historical fur trade on the ecosystem; because we think art will be more intuitive to show than tell in words. ', '28x43cm', 'Paper, Wood color pencil and Crayon'),
    ('Water in California ', 'Sims, Emma', 'This photo project captures the contrast in water usage, from the Bay Area, to Los Angeles. It also highlights the difference between where water comes from and where it is transported for urban use. ', 'Flat', 'Photography'),
    ('The Conflict on Board', 'Song, Shuhan;Li, Guozheng', 'The conflict between human and nature through the process of civilization is similar to the relationship between two chess players, with the continuing persistent conquering of wildness and how nature has been fighting back once and again. Using chess as a media to develop the relationship between environmentalism and capitalism, each chess piece is designed to represent a different character and their interactions with each other are shown on the board.', '15 x 15 x 1 inches', 'Chess, chess board and Gouache'),
    ('A Skewed Perception ', 'Arndt, Ariane ', 'Looking up at a truly dark night sky creates a sense of awe and reminds us that we are connected to this greater universe; however most of us have a skewed perception of the night sky as we live in heavily light polluted urban areas. While lights serve a useful purpose, the light pollution emitted physically separates us from the natural world by blocking our view of the night sky. This painting flips the typical scene of people stargazing and instead depicts a tree gazing at the city lights, similar to how we have flipped the natural night lighting of the earth. ', '12x15x1 inch ', 'Acrylics '),
    ('Religion in Ecosystem Management', 'Lee, Frank', 'This art depicts the differing belief systems between Native Americans and colonists, and how they were in conflict with each other and resulted in drastically different ecosystems. I used charcoal and pencil because it provided for the starkest contrast.', '5 x 10 x 15', 'Charcoal, Pencil'),
    ('The Ashes of Our Past/Alone', 'Li, Queenie', 'San Francisco\'s Embarcadero is an essential part of the City, but when we walk along it\'s famous piers, we have to wonder how much we have altered the picturesque view before us. "The Ashes of Our Past" shows these drastic alterations in such a way to evoke a feeling of loss by burning the top layer of the drawing; indeed, there is a loss of the romantic vision of a perfect, pristine landscape today. "Alone", the companion piece to "The Ashes of Our Past," is a more personal take on a burned photograph that hopefully many can relate to.', '11\'\' x 14\'\'/9.5\'\' x 11\'\'', 'Colored pencil, ink'),
    ('Exploring Anti-Chinese Sentiments Through Dance', 'Le, Mi;Yip, Helen', 'This performance piece explores anti-Chinese sentiment during the late 17th and early 20th century as a result of California\'s thriving resource economy. The Chinese conditions due to a high demand for labor led us to create a dance piece that expresses the oppression and structural discrimination against Asian Americans. ', '', 'Digital media'),
    ('Industrial-eyes', 'Tinoco, Carissa', 'Referencing a picture of Yosemite National Park\'s El Capitan as the base, I am making a statement on the effects of industrialization on environmental health. Included are some of three major industries in California: mining, water, and lumber/agriculture, each of which are represented by the mountains, the lake, and the trees/fallen log, respectively. The right half of the piece is a healthier environment and gradually becomes a polluted mess in the left half. ', '11"x13" paper', 'Colored pencils on paper'),
    ('Panning for resources: The successful development of California', 'Guo, Michelle;Kim, Nathan; Qi, Richard', ' We wanted to trace the extraction of resources that led to California’s continued success today. We depicted a series of miners panning in the Gold Rush environment, but instead of panning for just gold, the miners come up with a variety of items such as timber, fish, immigrants, railroads, etc. to modern day symbols such as the tech company logos which have contributed to the continued success of California’s Bay Area economy. This is accompanied with the issues and repercussions that each mined resource raised. Our artistic objectives include tracing California’s resources in a metaphoric and whimsical way, as well as providing social commentary when showing the subsequent environmental damage alongside aforementioned extraction. ', '11x14', 'colored pencil and pen'),
    ('The Tears of Generations ', 'Sullivan, Brendan ;Mcinerny, Brendan', 'In service of highlighting the injustice inflicted upon those who call the United States home. Separated by generations, the Cherokee Nation and modern day immigrants share a common foe--the United States Government. ', '16x20x1', 'Canvas and Paint '),
    ('The View from Above', 'Schellscheidt, June', 'HDR Photography. I am studying how vineyard owners create ecosystem security in the vineyards to ensure decent grape yields. Satellite imagery is used as a tool in order to adapt growth strategies.  ', '4 4x6 photos, maybe one 8x10', 'HDR Photography '),
    ('82 Midnight Suns', 'Conway, Anna', 'Jean, a young pilot starting her career, finds herself based in America\'s northernmost city, Barrow, Alaska. A Florida native, Jean expects the worst from the isolated state, but in turn develops a deep connection with the land and its people. Just as she becomes settled in her routine, a tragic event reveals the irony of Jean\'s work, bringing the raw relationship between imperial America and Iñupiaq people to the surface. Jean\'s time in Alaska exposes a world hardly known to the majority of Americans as well as the environmental and social consequences of capitalist venture and the "Manifest Destiny" complex. ', 'text', 'text'),
    ('Uprooted', 'Stephens, Cheyenne', 'This piece is meant to convey the relationship between the environment and humanity. The red represents human arteries. The tattered ends symbolize the attempted detachment of humans from nature. By denying the inseparability of the two, we are destroying ourselves along with our surroundings.', '37cm x 37cm x 1cm', 'Embroidery floss, linen'),
    ('Legacy', 'Ding, Xueting', 'Our generation leaves the scene on the left, looking forward to bright futures. But, we leave destruction in our wake; from fires to drought to pollutions, the Earth is left ravaged and dying.\nThe future generations walk in, entering the mess we\'ve left behind. Will they be able to live in this dying world?', '1 ft tall, 6 ft wide', 'Ipad app Procreate'),
    ('Mosaic Landscape', 'Hoage, Ariel', 'This piece integrates different gathered and found materials to explore the following questions. How do we see ourselves in relation to the natural world? How does this perspective change over time, and how does this change impact the physical landscapes we inhabit? How can we use different types of mapping and artistic representation to explore these concepts? ', '23" x 35" x 5"', 'Mixed media- Acrylic, Glass, Shell, Paper (papier mache and collage), plastic, dried house paint. adhesive '),
    ('Save Nature', 'Gaffney, Conall', 'My art shows the beauty of the natural world. It also explains the importance of the natural world to individuals and depicts how we are in grave danger.', '4 feet by 5 feet', 'Photography, printing'),
    ('The Gold Rush', 'Kim, Ashley', 'The Gold Rush attracted many immigrants to come to America to mine gold. However, the immigrants were disregarded. This artwork is to portray to story of immigrants through their skin. The reason why the immigrant’s skin color is not defined is because I want to represent the diverse racial groups of laborers from all over the world. ', '14" x 17"', 'Pencil, water color, color pencil, marker, sharpie'),
    ('Water Management in California ', 'Sepheri, Nika', 'I am a MCB and Math double major who appreciates art in all forms. Since I have started college I have not had a chance to practice art so I took advantage of this opportunity and made this piece for my final project.\nThis piece is a timeline for all of the important events, policies, and infrastructures that are related to water management in California. The timeline starts from 1848 and it goes until 2010. My goal is that people can picture and understand these events better, after having a visual representation.', '', 'Water color, colored pencils, and pen '),
    ('Tales from the Gold Mountain ', 'Mucho, Rachel', '"Tales from the Gold Mountain" depicts Chinese transcontinental railroad workers travelling through the Sierra Nevada mountains. The piece is done in a traditional Chinese watercolor style to depict the idealization of California in the late 1800s. The upper left corner depicts an old Chinese poem describing the sojourner experience. It reads: \n\nDispirited by life in my village home,\nI make a journey specially to the United States \n   of America.\nSeparated by mountains and passes, I feel an \n   extreme anxiety and grief;\nRushing about east and west does me no good.\nTurning in all directions—\nAn ideal opportunity has yet to come.\nIf fate is indeed Heaven\'s will, what more can \n   I say?\n\'Tis a disgrace to a man\'s pride and dignity.\n', '1920x1080 pixels', 'Photo manipulation and digital illustration'),
    ('Wild Fire', 'Meza Montoya, Gustavo', 'This song was inspired by the annecdotes from survivors in the recent wildfires that took place in Santa Rosa, California. The song reflects pain at the beginning and evolves to a reflective state by the end, in an effort to bridge an understanding with the environment to prevent any other disasters. ', 'n/a', 'The software used to mix all instrumentation was Garage band. Several instruments were used, along with a microphone and as well as some electronic music technology. '),
    ('Is vegetarianism cruelty free?', 'Garcia, Lizari', 'This purpose of this painting is to inform people about the effects that pesticides are having on people who live near were they are being sprayed. A study called CHAMACOS, done by UC Berkeley School of Public Health and Clinica de Salud del Valle de Salinas, started  about 16 years ago to show the negative effects that pesticides have on the people living in Salinas and the surrounding towns. Many things have been discovered but a lot of the people who live in Salinas are  illiterate so they can\'t read or understand the results, this is the reason that I decided to do an art project instead of a paper. The sky in this painting represents the negative impact that pesticides have on people, the mountains represents the environment, and the kids with different color clothes represent the kids who are part of the CHAMACOS study. The kids\' clothes are different colors because in the 1940\'s and 1950\'s when Cesar Chaves was advocating for field workers\'  rights the people would put a song while marching called "De colores," which literally means of colors. ', '16 by 20', 'oil paints, pictures of fields workers, and a canvas '),
    ('The Human and Crock', 'Xiao, Nan', 'From the Gold Rush Era to now, Environment is like a vessel of humanity. Sometimes, environment, as if a crock, contains our shapeless humanity; and sometimes, environment, as if a meduim, takes us from one place to another. ', 'unknown', 'Oil on Canvas '),
    ('Eutrophication in the Gulf of Mexico', 'Mehta, Monika', 'My art piece is supposed to represent eutrophication in the Gulf of Mexico. The dark part on the side is showing that run off fertilizer from farms and other areas that flow into the ocean is actually killing our reefs and native fish. This can affect the economy and natural ecosystems including birds that feed off of these fish.', '11x14', 'I used a canvas and watercolor paints.'),
    ('Worster\'s Theoretical Framework coming to life', 'Adler, Lila', 'Here is the depiction of Worster\'s theoretical framework coming to life. First the venn diagram to your left is an illustration of New Orlean\'s "instrumentalist" view on the use of nature. Next the center diagram is Hurricane Katrina followed by the shift towards "inter subjective" views on nature.', '10x22', 'Charcoal pencils, White canvas'),
    ('Field worker holding son\'s hand', 'Sanchez, David', 'This piece portrays a field worker holding their son\'s hand which represents the sacrifices they make for their families by working in such harsh conditions. The grapes represent the activism of field workers during the 1960s. I wanted to relate my work to the policies concerning immigration, DACA, and citizenship which is easy to think of in a solely political way, but I want to remind people that this is a much more personal matter.', '8x10 in', 'I used graphite pencils on sketch paper.'),
]

def parse_authors(authors_str):
    return seq(authors_str.split(';')) \
        .map(lambda last_first: tuple(x.strip() for x in last_first.split(','))) \
        .to_list()

def convert_data(row):
    title, authors_str, desc, size, material, box_id = row
    template = zot.item_template('artwork')
    # {'itemType': 'artwork', 'title': '', 'creators': [{'creatorType': 'artist', 'firstName': '', 'lastName': ''}], 'abstractNote': '', 'artworkMedium': '', 'artworkSize': '', 'date': '', 'language': '', 'shortTitle': '', 'archive': '', 'archiveLocation': '', 'libraryCatalog': '', 'callNumber': '', 'url': '', 'accessDate': '', 'rights': '', 'extra': '', 'tags': [], 'collections': [], 'relations': {}}

    template['title'] = title
    template['creators'] = seq(parse_authors(authors_str)) \
        .map(lambda last_first: {
            'creatorType': 'artist',
            'lastName': last_first[0],
            'firstName': last_first[1] }) \
        .to_list()

    template['abstractNote'] = desc
    template['artworkSize'] = size
    template['artworkMedium'] = material

    # template['tags'] = seq(tags.split(',')) \
    #     .map(lambda tag: 'raw:' + tag.strip()) \
    #     .map(make_tag).to_list()

    template['tags'].append(make_tag(SEMESTER_TAG)) # add semester tag

    template['url'] = BOX_URL_PREFIX + box_id
    return template

def folder_name(row):
    title, authors_str, _desc, _size, _material = map(lambda s: s.strip(), row)
    for ic in [ '/', '\\', '.', '..' ]:
        title = title.replace(ic, '_')
    authors_str = '; '.join(seq(parse_authors(authors_str))
        .map(lambda last_first: ', '.join(last_first)))
    return '{} by {}'.format(title, authors_str)



def sort_box_folders(pieces, box_folder_id, box_client, **kwargs):
    print('sorting box folders')
    folder = box_client.folder(box_folder_id)
    subfolders_dict = { f.name: f for f in folder.get_items() if f._item_type == 'folder' }
    box_files = box.list_all_files(folder)

    groups = { k: [] for k in pieces }
    ungrouped = []

    for box_file in box_files:
        def score(assign):
            a = box_file.name.lower()
            b = assign[1].lower()
            return similarity.substrsim(a, b)[1]
        best_piece = max(pieces, key=score)
        if score(best_piece) < 0.2:
            print('    NO GOOD PIECE FOUND FOR: ' + box_file.name)
            ungrouped.append(box_file)
        else:
            groups[best_piece].append(box_file)

    print()
    for k, fs in groups.items():
        print('  ' + str(k))
        for f in fs:
            print('    ' + f.name)
        print()

    # Move ungrouped files
    print('  moving ungrouped ({})'.format(len(ungrouped)))
    for f in ungrouped:
        f.move(folder)


    # Move grouped files
    print('  moving groups')
    new_pieces = []
    for piece, group in groups.items():
        if not group:
            print('    NO ITEMS FOUND FOR {}'.format(piece))
            continue # no items found

        subfolder_name = folder_name(piece)
        if subfolder_name in subfolders_dict:
            subfolder = subfolders_dict[subfolder_name]
        else:
            subfolder = folder.create_subfolder(subfolder_name)

        for f in group:
            f.move(subfolder)

        new_pieces.append(piece + (subfolder.id,))

    print('done sorting box folders')
    return new_pieces



def meta_to_zot(pieces, coll_id, **kwargs):
    print('creating item metadata in zotero')

    templates = seq(pieces) \
        .map(convert_data) \
        .to_list()
    items_resp = zot.create_items(templates)

    if (items_resp['failed']):
        print('Failed to create items:', items_resp['failed'])

    succ = items_resp['successful']
    for item in succ.values():
        zot.addto_collection(coll_id, item)

    print('done, created {} items'.format(len(succ)))

def files_to_zot(coll_id, box_client, **kwargs):
    print('moving files to zotero')

    items = [ x['data'] for x in zot.collection_items(coll_id) ]
    print('found {} items'.format(len(items)))

    attachments = {}
    parent_items = []
    for item in items:
        if 'parentItem' in item:
            parentId = item['parentItem']
            if parentId:
                attachments[parentId] = attachments.get(parentId, set())
                attachments[parentId].add(item['filename'])
                continue
        if 'url' not in item \
                or BOX_URL_PREFIX not in item['url'] \
                or item['url'].index(BOX_URL_PREFIX) != 0:
            print('  item has unknown url: {}'.format(item['key']))
            continue
        parent_items.append(item)

    for item in parent_items:
        folder_id = item['url'][len(BOX_URL_PREFIX):]
        folder = box_client.folder(folder_id)

        existing_attachments = attachments.get(item['key'], [])
        boxitems = [ x for x in folder.get_items() if x.name not in existing_attachments ]

        if not boxitems:
            print('  no new files to download for {}'.format(item['title']))
            continue

        print('  downloading {} files for {}'.format(len(boxitems), item['title']))
        with tempfile.TemporaryDirectory() as temp_dir:

            file_paths = [ os.path.join(temp_dir, boxitem.name) for boxitem in boxitems ]
            for file_path, boxitem in zip(file_paths, boxitems):
                print('    downloading {}'.format(boxitem.name))
                with open(file_path, 'wb') as temp_file:
                    boxitem.download_to(temp_file)

            print('  extracting')
            extracted_paths = extract_all(file_paths)
            print('    extracted {}'.format(len(extracted_paths)))

            print('  uploading to zotero')
            zot.attachment_simple(file_paths + extracted_paths, parentid=item['key'])

    print('done moving to zotero')




if __name__ == '__main__':
    kwargs = {}
    print('BOX', end=' ')
    kwargs['pieces'] = data
    kwargs['box_folder_id'] = BOX_INPUT_FOLDER
    kwargs['box_client'] = DevelopmentClient()
    coll = get_or_make_collection(COLLECTION_NAME)
    kwargs['coll_id'] = coll['key']

    kwargs['pieces'] = sort_box_folders(**kwargs)
    if coll['meta']['numItems'] <= 0: # TODO check this item by item
        meta_to_zot(**kwargs)
    files_to_zot(**kwargs)
