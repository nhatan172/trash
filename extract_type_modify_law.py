#!/usr/bin/env python
# -*- coding:utf8 -*-

from deepdive import *
import re
import handle_string
import divlaw

def lenIterator(list):
    sum = 0
    for i in list :
        sum += 1
    return sum
def getTitle(string):
    temp = re.finditer(r"\:(\s|\n|\*|\_|\#)*(\“|\")+.{2}",string,re.DOTALL)
    end_title = len(string)
    if lenIterator(temp) > 0 :
        temp = re.finditer(r"\:(\s|\n|\*|\_|\#)*(\“|\")",string,re.DOTALL)    
        for i in temp:
            end_title = i.start()
            break
    return string[:end_title]
def get_numerical_symbol(title):
    get_title1 = re.search(r'(của\s.*)\s(đã được|được)',title)
    get_title  = re.search(r'[0-9]+(/[0-9]+)*((/|-)[A-ZĐƯ]+[0-9]*)+(\s|\_|\#|\*|\.)',title,re.M|re.I)
    # get_id = re.search(r'[0-9]+(/[0-9]+)*((/|-)[A-ZĐ]+[0-9]*)+',get_content.group())
    # get_title1 = re.search(r'([0-9]+(/[0-9]+)*((/|-)[A-ZĐ]+[0-9]*)\s(đã được))|([0-9]+(/[0-9]+)*((/|-)[A-ZĐ]+[0-9]*)\s(được))',title)
    if(get_title1 is not None):
        number = re.search(r'[0-9]+(/[0-9]+)*((/|-)[A-ZĐƯ]+[0-9]*)+(\s|\_|\#|\*|\.)',get_title1.group())
        if(number is not None):
            return (re.search(r'[0-9]+(/[0-9]+)*((/|-)[A-ZĐƯ]+[0-9]*)+',number.group(),re.I)).group()
    elif (get_title is not None):
        return (re.search(r'[0-9]+(/[0-9]+)*((/|-)[A-ZĐƯ]+[0-9]*)+',get_title.group(),re.I)).group()
    return None
@tsv_extractor
@returns(lambda
    law_id ="text",
    type =  "int", 
    doc_content_update = "text",
    symbol = "text",
    position = "text",
    modified_law_date_release = "text" 
    :[])
def extract(
    law_id = "text",
    totalLaw = "int",
    law_content = "text", 
    law_len = "int",     
    totalItem  = "int",
    item_content = "text", 
    item_len = "int", 
    totalpoint = "int",
    point_content = "text",
    part_index ="int",
    chap_index ="int",
    sec_index ="int",
    law_index ="int",
    item_index ="int",
    point_index ="int",
    numerical_symbol = "text",
    date_released ="text"   
    ):
    
    doc_content_update = None

    if law_content is not None:
        # law_content = handle_string.to_unicode(law_content)
        law_content = law_content[:law_len]
        # pass
        # law_content = law_content.encode('utf-8')
    if (item_content is not None) :
    #     # item_content = handle_string.to_unicode(item_content)
    #     # if item_len != len(item_content):
        item_content = item_content[:item_len]
        # pass
        # item_content = item_content.encode('utf-8')
    number = None
    type = 0
    point = 0 
    p = re.compile(r'((((S|s)ửa đổi)(\s|\,)*((b|B)ổ sung)*)|((b|B)ổ sung))')
    p1= re.compile(r'(đã\s|đã được\s)((((S|s)ửa đổi)(\s|\,)*((b|B)ổ sung)*)|((b|B)ổ sung))')
    position = "0_0_0_0_0_0"
    if(totalpoint > 0):
        number = get_numerical_symbol(getTitle(point_content))
        if(number is not None):
            numerical_symbol = number
            date_released = None
        position = "{}_{}_{}_{}_{}_{}".format(part_index+1,chap_index+1,sec_index+1,law_index+1,item_index+1,point_index+1) 
        type_modify = re.search(r'(((b|B)ổ sung cụm từ)|((b|B)ổ sung từ))',point_content)
        if(type_modify is not None):
            type = 3
            doc_content_update = point_content
            point = 1
        else :
            type_change_name = re.search(r'(S|s)ửa đổi tên',point_content) 
            if(type_change_name is not None):
                type = 6
                doc_content_update = point_content
                point = 1
            else:
                type_delete = re.search(r'(b|B)ãi bỏ',point_content)
                inQuote = False
                if type_delete is not None :
                    inQuote = divlaw.itemInQuote(point_content,type_delete.start())
                if(type_delete is not None) and not inQuote:
                    type = 2
                    doc_content_update = point_content
                    point = 1
                else:
                    type_delete_text = re.search(r'(((b|B)ỏ cụm từ)|((b|B)ỏ từ))',point_content)
                    if(type_delete_text is not None):
                        type = 7
                        doc_content_update = point_content
                        point =1
                    else: 
                        type_add_text = p.finditer(point_content)
                        type_add_text1 = p1.finditer(point_content)
                        len1 = lenIterator(type_add_text)
                        len2 = lenIterator(type_add_text1)
                        if( (len1 != len2) and (len1 > 0)):
                            type = 1
                            doc_content_update = point_content
                            point = 1
                        else : 
                            # type_change_text = re.search(r'(t|T)hay\s.*cụm từ',point_content)
                            type_change_text = re.search(r'((t|T)hay\s)*(cụm\s)*từ\s.*(được\s)*(thay\s)*bằng\s(cụm\s)*từ',point_content)
                            if(type_change_text is not None):
                                type = 4
                                doc_content_update = point_content
                                point = 1
                            else : 
                                type_name_to_name = re.search(r'((t|T)ên của\s).+(((S|s)ửa đổi\s)(\,\s)*((b|B)ổ sung\s)*)(thành)',point_content)
                                if(type_name_to_name is not None):
                                    type = 5
                                    doc_content_update =point_content
                                    point = 1
                                else : 
                                    point = 0
    if(totalItem > 0 and point == 0):
        number = get_numerical_symbol(getTitle(item_content))
        if(number is not None):
            numerical_symbol = number
            date_released = None
        position = "{}_{}_{}_{}_{}_{}".format(part_index+1,chap_index+1,sec_index+1,law_index+1,item_index+1,0) 
        type_modify = re.search(r'(b|B)ổ sung cụm từ',item_content)
        if(type_modify is not None):
            type = 3
            doc_content_update = item_content
            point = 1
        else:
            type_change_name = re.search(r'(S|s)ửa đổi tên',item_content) 
            if(type_change_name is not None):
                type = 6
                doc_content_update = item_content
                point = 1
            else:
                type_delete = re.search(r'(b|B)ãi bỏ',item_content)
                inQuote = False
                if type_delete is not None :
                    inQuote = divlaw.itemInQuote(item_content,type_delete.start())
                if(type_delete is not None) and not inQuote:
                    type = 2
                    doc_content_update = item_content
                    point = 1
                else:
                    type_delete_text = re.search(r'(((b|B)ỏ cụm từ)|((b|B)ỏ từ))',item_content)
                    if(type_delete_text is not None):
                        type = 7
                        doc_content_update = item_content
                        point = 1
                    else: 
                        # type_add_text = re.search(r'((((S|s)ửa đổi)(\s|\,)*((b|B)ổ sung)*)|((b|B)ổ sung))',item_content)
                        # if(type_add_text is not None):
                        type_add_text = p.finditer(item_content)
                        type_add_text1 = p1.finditer(item_content)
                        len1 = lenIterator(type_add_text)
                        len2 = lenIterator(type_add_text1)
                        if( (len1 != len2) and (len1 > 0)):
                            type = 1
                            doc_content_update = item_content
                            point=1
                        else:
                            # type_change_text = re.search(r'(t|T)hay\s.*cụm từ',item_content)
                            type_change_text = re.search(r'((t|T)hay\s)*(cụm\s)*từ\s.*(được\s)*(thay\s)*bằng\s(cụm\s)*từ',item_content)
                            if(type_change_text is not None):
                                type = 4
                                doc_content_update = item_content
                                point = 1
                            else : 
                                type_name_to_name = re.search(r'((t|T)ên của\s).+(((S|s)ửa đổi\s)(\,\s)*((b|B)ổ sung\s)*)(thành)',item_content)
                                if(type_name_to_name is not None):
                                    type = 5
                                    doc_content_update = item_content
                                    point = 1
                                else : 
                                    point = 0
        # if(totalpoint > 0 and point == 1 ):
        #     doc_content_update = point_content
    if(totalLaw >0 and point == 0 ):
        number = get_numerical_symbol(getTitle(law_content))
        if(number is not None):
            numerical_symbol = number
            date_released = None
        position = "{}_{}_{}_{}_{}_{}".format(part_index+1,chap_index+1,sec_index+1,law_index+1,0,0) 
        type_modify = re.search(r'(b|B)ổ sung cụm từ',law_content)
        if(type_modify is not None):
            type = 3
            doc_content_update = law_content
            point = 1  
        else:
            type_change_name = re.search(r'(S|s)ửa đổi tên',law_content) 
            if(type_change_name is not None):
                type = 6
                doc_content_update = law_content
                point = 1
            else:
                type_delete = re.search(r'(b|B)ãi bỏ',law_content)
                inQuote = False
                if type_delete is not None :
                    inQuote = divlaw.itemInQuote(law_content,type_delete.start())
                if(type_delete is not None) and  not inQuote:
                    type = 2
                    doc_content_update = law_content
                    point = 1
                else:
                    type_delete_text = re.search(r'(((b|B)ỏ cụm từ)|((b|B)ỏ từ))',law_content)
                    if(type_delete_text is not None):
                        type = 7
                        doc_content_update = law_content
                        point = 1
                    else: 
                        type_add_text = p.finditer(law_content)
                        type_add_text1 = p1.finditer(law_content)
                        len1 = lenIterator(type_add_text)
                        len2 = lenIterator(type_add_text1)
                        if( (len1 != len2) and (len1 > 0)):
                            type = 1
                            doc_content_update = law_content
                            point = 1
                        else:
                            type_change_text = re.search(r'((t|T)hay\s)*(cụm\s)*từ\s.*(được\s)*(thay\s)*bằng\s(cụm\s)*từ',law_content)
                            if(type_change_text is not None):
                                type = 4
                                doc_content_update = law_content
                                point = 1
                            else : 
                                type_name_to_name = re.search(r'((t|T)ên của\s).+(((S|s)ửa đổi\s)(\,\s)*((b|B)ổ sung\s)*)(thành)',law_content)
                                if(type_name_to_name is not None):
                                    type = 5
                                    doc_content_update = law_content
                                    point = 1
                                else : 
                                    point = 0
        # if(totalItem > 0):
        #     doc_content_update = item_content
    if(point == 1):
        yield[
            law_id,
            type,
            doc_content_update,
            numerical_symbol,
            position,
            date_released
        ]
