from collections import defaultdict
import hashlib

from boxsdk import DevelopmentClient

import similarity as sim

FOLDER_ID = 57208387441
ACCESS_TOKEN = 'ofHPEG5EOCMHkHRS5x5aR8FBR8frXvlr'

OMEKA_KEY_IDENTITY = 'kepQQII5ovFhsHzqaHECL2x1cHV4a0Ov'
OMEKA_KEY_CREDENTIAL = 'mNT3napk9X3wPFyjr8gaQrN8m9T04XSq'

def list_all_files(folder, delete_empty=True):
    out = []
    items = folder.get_items()
    for item in items:
        if item._item_type == 'file':
            out.append(item)
        elif item._item_type == 'folder':
            out.extend(list_all_files(item))
    if len(out) == 0:
        folder.delete(recursive=False)
    return out


if __name__ == '__main__':
    client = DevelopmentClient()
    folder = client.folder(FOLDER_ID)

    files = list_all_files(folder)
    files_dict = { f.name: f for f in files }
    # Ignore zip files..
    files_names = [ f.name for f in files if not f.name.endswith('.zip') ]

    subfolders_dict = { f.name: f for f in folder.get_items() if f._item_type == 'folder' }

    # matched_files = defaultdict(lambda: [])
    # for f in files:
    #     sha1 = f.file_version.sha1
    #     matched_files[sha1].append(f)

    # for k, v in matched_files.items():
    #     if len(v) > 1:
    #         print(k, v)

    # subfolder = folder.create_subfolder('test_subfolder')
    # print(subfolder)

    grouped_filenames = sim.group_filenames(files_names)
    for group in grouped_filenames:
        rep_filename = max(group, key=len)
        rep = sim.remove_extension(rep_filename)
        print(rep)
        print(group)
        print()

        if rep in subfolders_dict:
            rep_folder = subfolders_dict[rep]
        else:
            rep_folder = folder.create_subfolder(rep)

        for filename in group:
            f = files_dict[filename]
            f.move(rep_folder)

    print('done')





# class Item:
#     def __init__(self):
#         self.authors = [('Ronan', 'Spreyer')]
#         self.year = 2018
#         self.title = 'Pikachu\'s Revenge'
#         self.sub_title = 'Surviving Charizard\'s crimsom dive'
#         self.type = 'Academic article'

#     def __str__(self):
#         auth = map(lambda tup: '{1}, {0}'.format(*tup), self.authors)
#         auth = '; '.join(auth)
#         return f'{auth} ({self.year}).  {self.title} - {self.sub_title}.  {self.type}'

#     def hash_id(self):
#         m = hashlib.sha1()
#         m.update(str(self).encode('utf-8'))
#         return m.digest().hex()
