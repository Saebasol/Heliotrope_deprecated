def remove_id_and_index_id(tag_or_file_list):
    response_dict_list = []
    for value in tag_or_file_list:
        del value["id"]
        del value["index_id"]
        response_dict_list.append(value)
    return response_dict_list
