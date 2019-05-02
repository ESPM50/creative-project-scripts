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
