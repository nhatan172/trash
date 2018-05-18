#!/usr/bin/env python
# -*- coding:utf8 -*-
from deepdive import *
import re
import divlaw
import handle_string

def lenIterator(list):
	sum = 0
	for i in list :
		sum += 1
		return sum

def getFirst(o):
	a = None
	for i in o:
		a = i
		break
	return a
def getTitle(string):
	temp = re.finditer(r"\:(\s|\n|\*|\_|\#)*(\“|\")",string,re.DOTALL)
	end_title = len(string)
	if divlaw.lenIterator(temp) > 0 :
		temp = re.finditer(r"\:(\s|\n|\*|\_|\#)*(\“|\")",string,re.DOTALL)
		for i in temp:
			end_title = i.start()
			break
			return string[:end_title]
def rewriteString(string):
	numberft = re.finditer(r"((\,\s)|(và\s))((\d+[a-zđ]{0,1})|([a-zđ]{1}))(?=(\s|\,|\.|\;))",string, re.U)
	a = divlaw.lenIterator(numberft)
	count = 0
	####################################
	while a > 0:
		if count >10 :
			return None
		numberft = re.finditer(r"((\,\s)|(và\s))((\d+[a-zđ]{0,1})|([a-zđ]{1}))(?=(\s|\,|\.|\;))",string, re.U)
		i = getFirst(numberft)
		startIndex = i.start()
		cutIndex = 0
		if string[startIndex] == ',' :
			cutIndex = startIndex + 2
			startIndex -= 1
		else :
			cutIndex = startIndex + 4
			startIndex -=2
		lastW = startIndex
		firstW = 0
		findLast = True
		while startIndex > 0:
			if string[startIndex] == ' ':
				if findLast :
					findLast = False
					lastW = startIndex
				else :
					firstW = startIndex + 1
					break
			startIndex -= 1
		string = string[:cutIndex] + string[firstW:lastW] + ' ' + string[cutIndex:]
		numberft = re.finditer(r"((\,\s)|(và\s))((\d+[a-zđ]{0,1})|([a-zđ]{1}))(?=(\s|\,|\.|\;))",string, re.U)
		a = divlaw.lenIterator(numberft)
		count += 1
	return writeDetail(string)
def writeDetail(string):
	numberft = re.finditer(r"điểm\s[a-zđ]{1}(?!\skhoản)",string, re.U)
	if divlaw.lenIterator(numberft) > 0:
		numberft = re.finditer(r"điểm\s[a-zđ]{1}(?!\skhoản)",string, re.U)
		addLen = 0
		for i in numberft:
			findItem = re.finditer(r"khoản\s\d+[a-zđ]?",string[i.end()+addLen:len(string)],re.U)
			if divlaw.lenIterator(findItem) > 0:
				findItem = re.finditer(r"khoản\s\d+[a-zđ]?",string[i.end()+addLen:len(string)],re.U)
				j = getFirst(findItem)
				if ' đ' in string[i.start():i.end()+1]:
					string = string[:i.end()+addLen+1] + " " + string[i.end()+j.start()+addLen:i.end()+j.end()+addLen] + string[1+i.end()+addLen:]
				else :
					string = string[:i.end()+addLen] + " " + string[i.end()+j.start()+addLen:i.end()+j.end()+addLen] + string[i.end()+addLen:]
				addLen += j.end() - j.start() + 1
			else :
				break
	numberft = re.finditer(r"khoản\s\d+[a-zđ]?(?!\sđiều)",string, re.U)
	if divlaw.lenIterator(numberft) > 0:
		numberft = re.finditer(r"khoản\s\d+[a-zđ]?(?!\sđiều)",string, re.U)
		addLen = 0
		for i in numberft:
			findItem = re.finditer(r"điều\s\d+[a-zđ]?",string[i.end()+addLen:len(string)],re.U)
			if divlaw.lenIterator(findItem) > 0:
				findItem = re.finditer(r"điều\s\d+[a-zđ]?",string[i.end()+addLen:len(string)],re.U)
				j = getFirst(findItem)
				string = string[:i.end()+addLen] + " " + string[i.end()+j.start()+addLen:i.end()+j.end()+addLen] + string[i.end()+addLen:]
				addLen += j.end() - j.start() + 1
			else :
				break
	return string
def divTitle(string):
	result = []
	findAddition = re.finditer(r"bổ\ssung\s.+vào",string,re.U)
	if divlaw.lenIterator(findAddition) > 0 :
		if ";" in string :
			findSemicomma = re.finditer(r"(bổ\ssung|sửa\sđổi).+\;",string,re.U)
			for i in findSemicomma:
				result.append(string[:i.end()])
				result.append(string[i.end():])
				break
		else :
			result.append(string)
	else :
		result.append(string)
	return result
@tsv_extractor
@returns(lambda
    law_id = "text",
    position = "text",
    type  = "int",
    part_modify_name ="text",
    chap_modify_name ="text",
    sec_modify_name ="text",
    law_modify_name ="text",
    item_modify_name ="text",
    point_modify_name ="text",
    text_delete ="text",
    from_text ="text",
    to_text ="text",
    symbol ="text",
    date = "text"
    :[])
def extract(
    law_id ="text",
    type_modify =  "int",
    content = "text",
	numerical_symbol = "text",
    position = "text",
    released_date = "text"   
    ):

	titles = getTitle(content)
	if type_modify == 1:
		titles = handle_string.toLowerCase(titles)
		###
		titles = rewriteString(titles)
		if titles is None:
			titles = "None"
			yield [
					law_id ,
					position,
					type_modify,
					"1",
					None,
					None,
					None,
					None,
					None,
					None,
					None,
					None,
					numerical_symbol,
					released_date
					]
		a = divTitle(titles)
		for title in a:
			findType = re.finditer(r"(.+vào.+)|(.+(sau|trước)[^\:]{7,})",title,re.U)
			if divlaw.lenIterator(findType) > 0:
				type_modify = 8
			match = re.finditer(r"(\n(\s|\_|\.|\*|\#)*\“(.(?!\“|\”))+.{2})|(\n(\s|\_|\.|\*|\#)*\"(.(?!\"))+.{2})", content,re.DOTALL)
			quotesIndex = []
			for i in match:
				quotesIndex.append(i.start())
			for j in range(len(quotesIndex)) :
				if type_modify == 1:
					divModify = divlaw.divPartModifyLaw(content)
					if j != (len(quotesIndex) - 1):
						divModify = divlaw.divPartModifyLaw(content[quotesIndex[j]:quotesIndex[j+1]])
					else :
						divModify = divlaw.divPartModifyLaw(content[quotesIndex[j]:])
					totalPart = divlaw.getTotalPart(divModify)
					if (totalPart == 0):
						totalPart = 1
					for part_id in range(0,totalPart):
						part = divlaw.getPart(divModify,part_id)
						if part['name'] != "":
							part_name = handle_string.toLowerCase(part['name'])
							if part_name in title:
								yield[
									law_id ,
									position,
									type_modify,
									part_name,
									None,
									None,
									None,
									None,
									None,
									None,
									None,
									None,
									numerical_symbol,
									released_date
									]
								continue
						totalChap = divlaw.getTotalChapter(divModify,part_id)
						if totalChap == 0:
							totalChap = 1
						for chap_id in range(0,totalChap):
							chap = divlaw.getChapter(divModify,part_id,chap_id)
							if chap['name'] != "":
								chap_name = handle_string.toLowerCase(chap['name'])
								if chap_name in title:
									part_name = None
									findName = re.finditer(r"(phần thứ)\s([A-z]|À|Á|Â|Ã|È|É|Ê|Ì|Í|Ò|Ó|Ô|Õ|Ù|Ú|Ă|Đ|Ĩ|Ũ|Ơ|à|á|â|ã|è|é|ê|ì|í|ò|ó|ô|õ|ù|ú|ă|đ|ĩ|ũ|ơ|Ư|Ă|Ạ|Ả|Ấ|Ầ|Ẩ|Ẫ|Ậ|Ắ|Ằ|Ẳ|Ẵ|Ặ|Ẹ|Ẻ|Ẽ|Ề|Ề|Ể|ư|ă|ạ|ả|ấ|ầ|ẩ|ẫ|ậ|ắ|ằ|ẳ|ẵ|ặ|ẹ|ẻ|ẽ|ề|ế|ể|Ễ|Ệ|Ỉ|Ị|Ọ|Ỏ|Ố|Ồ|Ổ|Ỗ|Ộ|Ớ|Ờ|Ở|Ỡ|Ợ|Ụ|Ủ|Ứ|Ừ|ễ|ệ|ỉ|ị|ọ|ỏ|ố|ồ|ổ|ỗ|ộ|ớ|ờ|ở|ỡ|ợ|ụ|ủ|ứ|ừ|Ử|Ữ|Ự|Ỳ|Ỵ|Ý|Ỷ|Ỹ|ử|ữ|ự|ỳ|ỵ|ỷ|ỹ)+",title)
									if divlaw.lenIterator(findName)>0 :
										findName = re.finditer(r"(phần thứ)\s([A-z]|À|Á|Â|Ã|È|É|Ê|Ì|Í|Ò|Ó|Ô|Õ|Ù|Ú|Ă|Đ|Ĩ|Ũ|Ơ|à|á|â|ã|è|é|ê|ì|í|ò|ó|ô|õ|ù|ú|ă|đ|ĩ|ũ|ơ|Ư|Ă|Ạ|Ả|Ấ|Ầ|Ẩ|Ẫ|Ậ|Ắ|Ằ|Ẳ|Ẵ|Ặ|Ẹ|Ẻ|Ẽ|Ề|Ề|Ể|ư|ă|ạ|ả|ấ|ầ|ẩ|ẫ|ậ|ắ|ằ|ẳ|ẵ|ặ|ẹ|ẻ|ẽ|ề|ế|ể|Ễ|Ệ|Ỉ|Ị|Ọ|Ỏ|Ố|Ồ|Ổ|Ỗ|Ộ|Ớ|Ờ|Ở|Ỡ|Ợ|Ụ|Ủ|Ứ|Ừ|ễ|ệ|ỉ|ị|ọ|ỏ|ố|ồ|ổ|ỗ|ộ|ớ|ờ|ở|ỡ|ợ|ụ|ủ|ứ|ừ|Ử|Ữ|Ự|Ỳ|Ỵ|Ý|Ỷ|Ỹ|ử|ữ|ự|ỳ|ỵ|ỷ|ỹ)+",title)
										for fN in findName:
											part_name = title[fN.span()[0]:fN.span()[1]]
											break
									yield[
									law_id ,
									position,
									type_modify,
									part_name,
								    chap_name,
								    None,
								    None,
								    None,
								    None,
								    None,
								    None,
								    None,
								    numerical_symbol,
								    released_date
									]
									continue
							totalSec = divlaw.getTotalSection(divModify,part_id,chap_id)
							if totalSec == 0:
								totalSec = 1
							for sec_id in range(0,totalSec):
								sec = divlaw.getSection(divModify, part_id, chap_id,sec_id)
								if sec['name'] != "":
									sec_name = handle_string.toLowerCase(sec['name'])
									if sec_name in title:
										part_name = None
										findName = re.finditer(r"(phần thứ)\s([A-z]|À|Á|Â|Ã|È|É|Ê|Ì|Í|Ò|Ó|Ô|Õ|Ù|Ú|Ă|Đ|Ĩ|Ũ|Ơ|à|á|â|ã|è|é|ê|ì|í|ò|ó|ô|õ|ù|ú|ă|đ|ĩ|ũ|ơ|Ư|Ă|Ạ|Ả|Ấ|Ầ|Ẩ|Ẫ|Ậ|Ắ|Ằ|Ẳ|Ẵ|Ặ|Ẹ|Ẻ|Ẽ|Ề|Ề|Ể|ư|ă|ạ|ả|ấ|ầ|ẩ|ẫ|ậ|ắ|ằ|ẳ|ẵ|ặ|ẹ|ẻ|ẽ|ề|ế|ể|Ễ|Ệ|Ỉ|Ị|Ọ|Ỏ|Ố|Ồ|Ổ|Ỗ|Ộ|Ớ|Ờ|Ở|Ỡ|Ợ|Ụ|Ủ|Ứ|Ừ|ễ|ệ|ỉ|ị|ọ|ỏ|ố|ồ|ổ|ỗ|ộ|ớ|ờ|ở|ỡ|ợ|ụ|ủ|ứ|ừ|Ử|Ữ|Ự|Ỳ|Ỵ|Ý|Ỷ|Ỹ|ử|ữ|ự|ỳ|ỵ|ỷ|ỹ)+",title)
										if divlaw.lenIterator(findName)>0 :
											findName = re.finditer(r"(phần thứ)\s([A-z]|À|Á|Â|Ã|È|É|Ê|Ì|Í|Ò|Ó|Ô|Õ|Ù|Ú|Ă|Đ|Ĩ|Ũ|Ơ|à|á|â|ã|è|é|ê|ì|í|ò|ó|ô|õ|ù|ú|ă|đ|ĩ|ũ|ơ|Ư|Ă|Ạ|Ả|Ấ|Ầ|Ẩ|Ẫ|Ậ|Ắ|Ằ|Ẳ|Ẵ|Ặ|Ẹ|Ẻ|Ẽ|Ề|Ề|Ể|ư|ă|ạ|ả|ấ|ầ|ẩ|ẫ|ậ|ắ|ằ|ẳ|ẵ|ặ|ẹ|ẻ|ẽ|ề|ế|ể|Ễ|Ệ|Ỉ|Ị|Ọ|Ỏ|Ố|Ồ|Ổ|Ỗ|Ộ|Ớ|Ờ|Ở|Ỡ|Ợ|Ụ|Ủ|Ứ|Ừ|ễ|ệ|ỉ|ị|ọ|ỏ|ố|ồ|ổ|ỗ|ộ|ớ|ờ|ở|ỡ|ợ|ụ|ủ|ứ|ừ|Ử|Ữ|Ự|Ỳ|Ỵ|Ý|Ỷ|Ỹ|ử|ữ|ự|ỳ|ỵ|ỷ|ỹ)+",title)
											for fN in findName:
												part_name = title[fN.span()[0]:fN.span()[1]]
												break
										chap_name = None
										findName = re.finditer(r"(chương)\s([A-Z]|[0-9])+",title)
										if divlaw.lenIterator(findName)>0 :
											findName = re.finditer(r"(chương)\s([A-Z]|[0-9])+",title)
											for fN in findName:
												chap['name'] = title[fN.span()[0]:fN.span()[1]]
												break
										yield[
										law_id ,
    									position,
										type_modify,
										part_name,
									    chap_name,
									    sec_name,
									    None,
									    None,
									    None,
									    None,
									    None,
									    None,
										numerical_symbol,
										released_date
										]
										continue
								totalLaw = divlaw.getTotalLaw(divModify,part_id,chap_id,sec_id)
								if totalLaw == 0:
									totalLaw = 1
								for law_index in range(0,totalSec):
									law = divlaw.getLaw(divModify,part_id,chap_id,sec_id,law_index)
									if law['name'] != "":
										law_name = handle_string.toLowerCase(law['name'])
										if law_name in title:
											part_name = None
											findName = re.finditer(r"(phần thứ)\s([A-z]|À|Á|Â|Ã|È|É|Ê|Ì|Í|Ò|Ó|Ô|Õ|Ù|Ú|Ă|Đ|Ĩ|Ũ|Ơ|à|á|â|ã|è|é|ê|ì|í|ò|ó|ô|õ|ù|ú|ă|đ|ĩ|ũ|ơ|Ư|Ă|Ạ|Ả|Ấ|Ầ|Ẩ|Ẫ|Ậ|Ắ|Ằ|Ẳ|Ẵ|Ặ|Ẹ|Ẻ|Ẽ|Ề|Ề|Ể|ư|ă|ạ|ả|ấ|ầ|ẩ|ẫ|ậ|ắ|ằ|ẳ|ẵ|ặ|ẹ|ẻ|ẽ|ề|ế|ể|Ễ|Ệ|Ỉ|Ị|Ọ|Ỏ|Ố|Ồ|Ổ|Ỗ|Ộ|Ớ|Ờ|Ở|Ỡ|Ợ|Ụ|Ủ|Ứ|Ừ|ễ|ệ|ỉ|ị|ọ|ỏ|ố|ồ|ổ|ỗ|ộ|ớ|ờ|ở|ỡ|ợ|ụ|ủ|ứ|ừ|Ử|Ữ|Ự|Ỳ|Ỵ|Ý|Ỷ|Ỹ|ử|ữ|ự|ỳ|ỵ|ỷ|ỹ)+",title)
											if divlaw.lenIterator(findName)>0 :
												findName = re.finditer(r"(phần thứ)\s([A-z]|À|Á|Â|Ã|È|É|Ê|Ì|Í|Ò|Ó|Ô|Õ|Ù|Ú|Ă|Đ|Ĩ|Ũ|Ơ|à|á|â|ã|è|é|ê|ì|í|ò|ó|ô|õ|ù|ú|ă|đ|ĩ|ũ|ơ|Ư|Ă|Ạ|Ả|Ấ|Ầ|Ẩ|Ẫ|Ậ|Ắ|Ằ|Ẳ|Ẵ|Ặ|Ẹ|Ẻ|Ẽ|Ề|Ề|Ể|ư|ă|ạ|ả|ấ|ầ|ẩ|ẫ|ậ|ắ|ằ|ẳ|ẵ|ặ|ẹ|ẻ|ẽ|ề|ế|ể|Ễ|Ệ|Ỉ|Ị|Ọ|Ỏ|Ố|Ồ|Ổ|Ỗ|Ộ|Ớ|Ờ|Ở|Ỡ|Ợ|Ụ|Ủ|Ứ|Ừ|ễ|ệ|ỉ|ị|ọ|ỏ|ố|ồ|ổ|ỗ|ộ|ớ|ờ|ở|ỡ|ợ|ụ|ủ|ứ|ừ|Ử|Ữ|Ự|Ỳ|Ỵ|Ý|Ỷ|Ỹ|ử|ữ|ự|ỳ|ỵ|ỷ|ỹ)+",title)
												for fN in findName:
													part_name = title[fN.span()[0]:fN.span()[1]]
													break
											chap_name = None
											findName = re.finditer(r"(chương)\s([A-Z]|[0-9])+",title)
											if divlaw.lenIterator(findName)>0 :
												findName = re.finditer(r"(chương)\s([A-Z]|[0-9])+",title)
												for fN in findName:
													chap_name = title[fN.span()[0]:fN.span()[1]]
													break
											sec_name = None
											findName = re.finditer(r"(mục)\s([A-Z]|[0-9])+",title)
											if divlaw.lenIterator(findName)>0 :
												findName = re.finditer(r"(mục)\s([A-Z]|[0-9])+",title)
												for fN in findName:
													sec_name = title[fN.span()[0]:fN.span()[1]]
													break
											yield[
											law_id ,
    										position,
											type_modify,
										    part_name,
										    chap_name,
										    sec_name,
										    law_name,
										    None,
										    None,
										    None,
										    None,
										    None,
										    numerical_symbol,
										    released_date
											]
											continue
									totalItem = divlaw.getTotalItem(divModify,part_id,chap_id,sec_id,law_index)
									if totalItem == 0:
										totalItem = 1
									for item_id in range(0,totalItem):
										item = divlaw.getItem(divModify,part_id,chap_id,sec_id,law_index,item_id)
										if item['name'] != "":
											item_name = 'khoản ' + item['name']
											if item_name in title:
												find_item_name = re.finditer(r"khoản\s"+item['name'],title,re.U)
												ex = getFirst(find_item_name)
												index_start = ex.end()
												part_name = None
												findName = re.finditer(r"(phần thứ)\s([A-z]|À|Á|Â|Ã|È|É|Ê|Ì|Í|Ò|Ó|Ô|Õ|Ù|Ú|Ă|Đ|Ĩ|Ũ|Ơ|à|á|â|ã|è|é|ê|ì|í|ò|ó|ô|õ|ù|ú|ă|đ|ĩ|ũ|ơ|Ư|Ă|Ạ|Ả|Ấ|Ầ|Ẩ|Ẫ|Ậ|Ắ|Ằ|Ẳ|Ẵ|Ặ|Ẹ|Ẻ|Ẽ|Ề|Ề|Ể|ư|ă|ạ|ả|ấ|ầ|ẩ|ẫ|ậ|ắ|ằ|ẳ|ẵ|ặ|ẹ|ẻ|ẽ|ề|ế|ể|Ễ|Ệ|Ỉ|Ị|Ọ|Ỏ|Ố|Ồ|Ổ|Ỗ|Ộ|Ớ|Ờ|Ở|Ỡ|Ợ|Ụ|Ủ|Ứ|Ừ|ễ|ệ|ỉ|ị|ọ|ỏ|ố|ồ|ổ|ỗ|ộ|ớ|ờ|ở|ỡ|ợ|ụ|ủ|ứ|ừ|Ử|Ữ|Ự|Ỳ|Ỵ|Ý|Ỷ|Ỹ|ử|ữ|ự|ỳ|ỵ|ỷ|ỹ)+",title[index_start:])
												if divlaw.lenIterator(findName)>0 :
													findName = re.finditer(r"(phần thứ)\s([A-z]|À|Á|Â|Ã|È|É|Ê|Ì|Í|Ò|Ó|Ô|Õ|Ù|Ú|Ă|Đ|Ĩ|Ũ|Ơ|à|á|â|ã|è|é|ê|ì|í|ò|ó|ô|õ|ù|ú|ă|đ|ĩ|ũ|ơ|Ư|Ă|Ạ|Ả|Ấ|Ầ|Ẩ|Ẫ|Ậ|Ắ|Ằ|Ẳ|Ẵ|Ặ|Ẹ|Ẻ|Ẽ|Ề|Ề|Ể|ư|ă|ạ|ả|ấ|ầ|ẩ|ẫ|ậ|ắ|ằ|ẳ|ẵ|ặ|ẹ|ẻ|ẽ|ề|ế|ể|Ễ|Ệ|Ỉ|Ị|Ọ|Ỏ|Ố|Ồ|Ổ|Ỗ|Ộ|Ớ|Ờ|Ở|Ỡ|Ợ|Ụ|Ủ|Ứ|Ừ|ễ|ệ|ỉ|ị|ọ|ỏ|ố|ồ|ổ|ỗ|ộ|ớ|ờ|ở|ỡ|ợ|ụ|ủ|ứ|ừ|Ử|Ữ|Ự|Ỳ|Ỵ|Ý|Ỷ|Ỹ|ử|ữ|ự|ỳ|ỵ|ỷ|ỹ)+",title[index_start:])
													for fN in findName:
														part_name = title[index_start+fN.span()[0]:index_start+fN.span()[1]]
														break
												chap_name = None
												findName = re.finditer(r"(chương)\s([A-Z]|[0-9])+",title[index_start:])
												if divlaw.lenIterator(findName)>0 :
													findName = re.finditer(r"(chương)\s([A-Z]|[0-9])+",title[index_start:])
													for fN in findName:
														chap_name = title[index_start+fN.span()[0]:index_start+fN.span()[1]]
														break
												sec_name = None
												findName = re.finditer(r"(mục)\s([A-Z]|[0-9])+",title[index_start:])
												if divlaw.lenIterator(findName)>0 :
													findName = re.finditer(r"(mục)\s([A-Z]|[0-9])+",title[index_start:])
													for fN in findName:
														sec_name = title[index_start+fN.span()[0]:index_start+fN.span()[1]]
														break
												law_name = None
												findName = re.finditer(r"điều [0-9]+\w*",title[index_start:])
												if divlaw.lenIterator(findName)>0 :
													findName = re.finditer(r"điều [0-9]+\w*",title[index_start:])
													for fN in findName:
														law_name = title[index_start+fN.span()[0]:index_start+fN.span()[1]]
														break
												yield[
												law_id ,
    											position,
												type_modify,
											    part_name,
											    chap_name,
											    sec_name,
											    law_name,
											    item['name'],
											    None,
											    None,
											    None,
											    None,
											    numerical_symbol,
											    released_date
												]
												continue
										totalPoint = divlaw.getTotalPoint(divModify,part_id,chap_id,sec_id,law_index,item_id)
										if totalPoint == 0:
											totalPoint = 1
										for point_id in range(0,totalPoint):
											point = divlaw.getPoint(divModify,part_id,chap_id,sec_id,law_index,item_id,point_id)
											if point['name'] != "":
												point_name = 'điểm ' + point['name']
												if point_name in title:
													find_point_name = re.finditer(r"điểm "+point['name'],title,re.U)
													index_start = getFirst(find_point_name).end()
													part_name = None
													findName = re.finditer(r"(phần thứ)\s([A-z]|À|Á|Â|Ã|È|É|Ê|Ì|Í|Ò|Ó|Ô|Õ|Ù|Ú|Ă|Đ|Ĩ|Ũ|Ơ|à|á|â|ã|è|é|ê|ì|í|ò|ó|ô|õ|ù|ú|ă|đ|ĩ|ũ|ơ|Ư|Ă|Ạ|Ả|Ấ|Ầ|Ẩ|Ẫ|Ậ|Ắ|Ằ|Ẳ|Ẵ|Ặ|Ẹ|Ẻ|Ẽ|Ề|Ề|Ể|ư|ă|ạ|ả|ấ|ầ|ẩ|ẫ|ậ|ắ|ằ|ẳ|ẵ|ặ|ẹ|ẻ|ẽ|ề|ế|ể|Ễ|Ệ|Ỉ|Ị|Ọ|Ỏ|Ố|Ồ|Ổ|Ỗ|Ộ|Ớ|Ờ|Ở|Ỡ|Ợ|Ụ|Ủ|Ứ|Ừ|ễ|ệ|ỉ|ị|ọ|ỏ|ố|ồ|ổ|ỗ|ộ|ớ|ờ|ở|ỡ|ợ|ụ|ủ|ứ|ừ|Ử|Ữ|Ự|Ỳ|Ỵ|Ý|Ỷ|Ỹ|ử|ữ|ự|ỳ|ỵ|ỷ|ỹ)+",title[index_start:])
													if divlaw.lenIterator(findName)>0 :
														findName = re.finditer(r"(phần thứ)\s([A-z]|À|Á|Â|Ã|È|É|Ê|Ì|Í|Ò|Ó|Ô|Õ|Ù|Ú|Ă|Đ|Ĩ|Ũ|Ơ|à|á|â|ã|è|é|ê|ì|í|ò|ó|ô|õ|ù|ú|ă|đ|ĩ|ũ|ơ|Ư|Ă|Ạ|Ả|Ấ|Ầ|Ẩ|Ẫ|Ậ|Ắ|Ằ|Ẳ|Ẵ|Ặ|Ẹ|Ẻ|Ẽ|Ề|Ề|Ể|ư|ă|ạ|ả|ấ|ầ|ẩ|ẫ|ậ|ắ|ằ|ẳ|ẵ|ặ|ẹ|ẻ|ẽ|ề|ế|ể|Ễ|Ệ|Ỉ|Ị|Ọ|Ỏ|Ố|Ồ|Ổ|Ỗ|Ộ|Ớ|Ờ|Ở|Ỡ|Ợ|Ụ|Ủ|Ứ|Ừ|ễ|ệ|ỉ|ị|ọ|ỏ|ố|ồ|ổ|ỗ|ộ|ớ|ờ|ở|ỡ|ợ|ụ|ủ|ứ|ừ|Ử|Ữ|Ự|Ỳ|Ỵ|Ý|Ỷ|Ỹ|ử|ữ|ự|ỳ|ỵ|ỷ|ỹ)+",title[index_start:])
														for fN in findName:
															part_name = title[index_start+fN.span()[0]:index_start+fN.span()[1]]
															break
													chap_name = None
													findName = re.finditer(r"(chương)\s([A-Z]|[0-9])+",title[index_start:])
													if divlaw.lenIterator(findName)>0 :
														findName = re.finditer(r"(chương)\s([A-Z]|[0-9])+",title[index_start:])
														for fN in findName:
															chap_name = title[index_start+fN.span()[0]:index_start+fN.span()[1]]
															break
													sec_name = None
													findName = re.finditer(r"(mục)\s([A-Z]|[0-9])+",title[index_start:])
													if divlaw.lenIterator(findName)>0 :
														findName = re.finditer(r"(mục)\s([A-Z]|[0-9])+",title[index_start:])
														for fN in findName:
															sec_name = title[index_start+fN.span()[0]:index_start+fN.span()[1]]
															break
													law_name = None
													findName = re.finditer(r"điều [0-9]+\w*",title[index_start:])
													if divlaw.lenIterator(findName)>0 :
														findName = re.finditer(r"điều [0-9]+\w*",title[index_start:])
														for fN in findName:
															law_name = title[index_start+fN.span()[0]:index_start+fN.span()[1]]
															break
													item_name = None
													findName = re.finditer(r"(?:khoản\s)[0-9]+\w*",title[index_start:])
													if divlaw.lenIterator(findName)>0 :
														findName = re.finditer(r"(?:khoản\s)[0-9]+\w*",title[index_start:])
														for fN in findName:
															item_name = title[index_start+8+fN.span()[0]:index_start+fN.span()[1]]
															break
													yield[
												    law_id ,
													position,
													type_modify,
												    part_name,
												    chap_name,
												    sec_name,
												    law_name,
												    item_name,
												    point['name'],
												    None,
												    None,
												    None,
												    numerical_symbol,
												    released_date
													]
													continue
				if type_modify == 8:
					start_index = 0
					ft = re.finditer(r"bổ\ssung\s.+(vào).{5}",title,re.U)
					for i in ft :
						start_index = i.end() - 5
						break
					ft = re.finditer(r"bổ\ssung\s.+(sau|trước).{5}",title,re.U)
					for i in ft :
						start_index = i.end() - 5
						break
					part_name = None
					findName = re.finditer(r"(phần thứ)\s([A-z]|À|Á|Â|Ã|È|É|Ê|Ì|Í|Ò|Ó|Ô|Õ|Ù|Ú|Ă|Đ|Ĩ|Ũ|Ơ|à|á|â|ã|è|é|ê|ì|í|ò|ó|ô|õ|ù|ú|ă|đ|ĩ|ũ|ơ|Ư|Ă|Ạ|Ả|Ấ|Ầ|Ẩ|Ẫ|Ậ|Ắ|Ằ|Ẳ|Ẵ|Ặ|Ẹ|Ẻ|Ẽ|Ề|Ề|Ể|ư|ă|ạ|ả|ấ|ầ|ẩ|ẫ|ậ|ắ|ằ|ẳ|ẵ|ặ|ẹ|ẻ|ẽ|ề|ế|ể|Ễ|Ệ|Ỉ|Ị|Ọ|Ỏ|Ố|Ồ|Ổ|Ỗ|Ộ|Ớ|Ờ|Ở|Ỡ|Ợ|Ụ|Ủ|Ứ|Ừ|ễ|ệ|ỉ|ị|ọ|ỏ|ố|ồ|ổ|ỗ|ộ|ớ|ờ|ở|ỡ|ợ|ụ|ủ|ứ|ừ|Ử|Ữ|Ự|Ỳ|Ỵ|Ý|Ỷ|Ỹ|ử|ữ|ự|ỳ|ỵ|ỷ|ỹ)+",title[start_index:])
					if divlaw.lenIterator(findName)>0 :
						findName = re.finditer(r"(phần thứ)\s([A-z]|À|Á|Â|Ã|È|É|Ê|Ì|Í|Ò|Ó|Ô|Õ|Ù|Ú|Ă|Đ|Ĩ|Ũ|Ơ|à|á|â|ã|è|é|ê|ì|í|ò|ó|ô|õ|ù|ú|ă|đ|ĩ|ũ|ơ|Ư|Ă|Ạ|Ả|Ấ|Ầ|Ẩ|Ẫ|Ậ|Ắ|Ằ|Ẳ|Ẵ|Ặ|Ẹ|Ẻ|Ẽ|Ề|Ề|Ể|ư|ă|ạ|ả|ấ|ầ|ẩ|ẫ|ậ|ắ|ằ|ẳ|ẵ|ặ|ẹ|ẻ|ẽ|ề|ế|ể|Ễ|Ệ|Ỉ|Ị|Ọ|Ỏ|Ố|Ồ|Ổ|Ỗ|Ộ|Ớ|Ờ|Ở|Ỡ|Ợ|Ụ|Ủ|Ứ|Ừ|ễ|ệ|ỉ|ị|ọ|ỏ|ố|ồ|ổ|ỗ|ộ|ớ|ờ|ở|ỡ|ợ|ụ|ủ|ứ|ừ|Ử|Ữ|Ự|Ỳ|Ỵ|Ý|Ỷ|Ỹ|ử|ữ|ự|ỳ|ỵ|ỷ|ỹ)+",title[start_index:])
						for fN in findName:
							part_name = title[start_index+fN.span()[0]:start_index+fN.span()[1]]
							break
					chap_name = None
					findName = re.finditer(r"(chương)\s([A-Z]|[0-9])+",title[start_index:])
					if divlaw.lenIterator(findName)>0 :
						findName = re.finditer(r"(chương)\s([A-Z]|[0-9])+",title[start_index:])
						for fN in findName:
							chap_name = title[start_index+fN.span()[0]:start_index+fN.span()[1]]
							break
					sec_name = None
					findName = re.finditer(r"(mục)\s([A-Z]|[0-9])+",title[start_index:])
					if divlaw.lenIterator(findName)>0 :
						findName = re.finditer(r"(mục)\s([A-Z]|[0-9])+",title[start_index:])
						for fN in findName:
							sec_name = title[start_index+fN.span()[0]:start_index+fN.span()[1]]
							break
					law_name = None
					findName = re.finditer(r"điều [0-9]+[A-zĐđ]*",title[start_index:])
					if divlaw.lenIterator(findName)>0 :
						findName = re.finditer(r"điều [0-9]+[A-zĐđ]*",title[start_index:])
						for fN in findName:
							law_name = title[start_index+fN.span()[0]:start_index+fN.span()[1]]
							break
					item_name = None
					findName = re.finditer(r"(khoản\s)[0-9]+",title[start_index:])
					if divlaw.lenIterator(findName)>0 :
						findName = re.finditer(r"(khoản\s)[0-9]+",title[start_index:])
						for fN in findName:
							item_name = title[start_index+fN.span()[0] + 8:start_index+fN.span()[1]]
							break
					point_name = None
					temp = title
					findName = re.finditer(r"(điểm\s)[A-z]+",title[start_index:],re.U)
					if divlaw.lenIterator(findName) > 0 :
						findName = re.finditer(r"(điểm\s)[A-zđ]+",temp[start_index:],re.U)
						for fN in findName:
							point_name = temp[start_index+fN.span()[0]:start_index+fN.span()[0]]
							break
					if 'sau' in title[:start_index]:
						type_modify = 9
					elif 'trước' in title[:start_index]:
						type_modify = 10
					yield[
					    law_id ,
						position,
						type_modify,
					    part_name,
					    chap_name,
					    sec_name,
					    law_name,
					    item_name,
					    point_name,
					    None,
					    None,
					    None,
					    numerical_symbol,
					    released_date
					]

	if type_modify == 2 :
		t = re.compile(r'(Đ|đ)iểm\s(\w{1,5}|\d{1,5})\s(k|K)hoản\s(\w{1,5}|\d{1,5})\s(Đ|đ)iều\s((\w{1,5})|(\d{1,5}))|(k|K)hoản\s(\w{1,5}|\d{1,5})\s(Đ|đ)iều\s((\w{1,5})|(\d{1,5}))|(đ|Đ)iều\s((\w{1,5})|(\d{1,5}))')
		extract = t.finditer(content)
		if(lenIterator(extract)>0):
			for extract in t.finditer(content):
				temp_law = re.search(r'(đ|Đ)iều\s((\d{1,5})([a-zđ]|[A-Z])?)',content[extract.span()[0]:extract.span()[1]])
				if(temp_law is not None):
					law = temp_law.group()
				else :
					law = None
				temp_item = re.search(r'(Khoản|khoản)\s(\w{1,5}|\d{1,5})',content[extract.span()[0]:extract.span()[1]])
			if(temp_item is not None):
				item = temp_item.group()[8:]
			else :
			    item = None
			temp_point = re.search(r'(đ|Đ)iểm\s(\w{1,5}|\d{1,5})',content[extract.span()[0]:extract.span()[1]])
			if(temp_point is not None):
			    point = temp_point.group()[8:]
			else :
			    point = None
			yield[
			    law_id,
			    position,
				type_modify,
			    None,
			    None,
			    None,
			    law,
			    item,
			    point,
			    None,
			    None,
			    None,
			    numerical_symbol,
			    released_date
			]
		else :
		    yield[
		        law_id,
		        position,
				type_modify,
		        None,
		        None,
		        None,
		        None,
		        None,
		        None,
		        None,
		        None,
		        None,
		        numerical_symbol,
		        released_date
		    ]
	if(type_modify == 3 ):
		p =re.compile(r'(B|b)ổ\ssung\s(cụm\s)*từ\s')
		for location in p.finditer(content):
		    sub_content = content[location.span()[1]:len(content)]
		    temp = p.finditer(sub_content)
		    if(lenIterator(temp)>0):
		        for temp in p.finditer(sub_content):
		            sub_content = sub_content[0:temp.span()[0]]
		            break
		    temp_replace = re.search(r'(\“|\")(\s)*.+(\s)*(\”|\")\s.*sau\s(cụm\s)*từ\s',sub_content)
		    if(temp_replace is not None):
		        temp_from_replace = re.search(r'(\“|\")(\s)*.+(\s)*(\”|\")',temp_replace.group())
		        from_replace = temp_from_replace.group()
		        temp_replace = re.search(r'sau\s(cụm\s)*từ\s(\“|\")(\s)*.+(\s)*(\”|\")',sub_content)
		        temp_to_replace = re.search(r'(\“|\")(\s)*.+(\s)*(\”|\")',temp_replace.group())
		        to_replace = temp_to_replace.group()
		        t = re.compile(r'(Đ|đ)iểm\s(\w{1,5}|\d{1,5})\s(k|K)hoản\s(\w{1,5}|\d{1,5})\s(Đ|đ)iều\s((\w{1,5})|(\d{1,5}))|(k|K)hoản\s(\w{1,5}|\d{1,5})\s(Đ|đ)iều\s((\w{1,5})|(\d{1,5}))|(đ|Đ)iều\s((\w{1,5})|(\d{1,5}))')
		        extract = t.finditer(sub_content,re.DOTALL)
		        if(lenIterator(extract)>0):
		            for extract in t.finditer(sub_content):
		                temp_law = re.search(r'(đ|Đ)iều\s((\d{1,5})([a-zđ]|[A-Z])?)',sub_content[extract.span()[0]:extract.span()[1]])
		                if(temp_law is not None):
		                    law = temp_law.group()
		                else :
		                    law = None
		                temp_item = re.search(r'(Khoản|khoản)\s(\w{1,5}|\d{1,5})',sub_content[extract.span()[0]:extract.span()[1]])
		                if(temp_item is not None):
		                    item = temp_item.group()[8:]
		                else :
		                    item = None
		                temp_point = re.search(r'(đ|Đ)iểm\s(\w{1,5}|\d{1,5})',sub_content[extract.span()[0]:extract.span()[1]])
		                if(temp_point is not None):
		                    point = temp_point.group()[8:]
		                else :
		                    point = None
		                yield[
		                    law_id,
		                    position,
							type_modify,
		                    None,
		                    None,
		                    None,
		                    law,
		                    item,
		                    point,
		                    sub_content,
		                    from_replace,
		                    to_replace,
		                    numerical_symbol,
		                    released_date
		                ]
			else :
			    yield[
			        law_id,
			        position,
					type_modify,
			        None,
			        None,
			        None,
			        None,
			        None,
			        None,
			        None,
			        None,
			        None,
			        numerical_symbol,
			        released_date
			    ]
	if(type_modify == 4 ):
	    p =re.compile(r'((t|T)hay\s)*(cụm\s)*từ\s')
	    for location in p.finditer(content):
	        sub_content = content[location.span()[1]:len(content)]
	        temp = p.finditer(sub_content)
	        if(lenIterator(temp)>0):
	            for temp in p.finditer(sub_content):
	            	# sub_content_from : lấy cụm từ cần sửa đổi để tách 
	                sub_content_from = sub_content[0:temp.span()[1]]
	                break
	        temp_replace = re.search(r'(\“|\")(\s)*.+(\s)*(\”|\")\s.*(được\s)*(thay\s)*bằng\s(cụm\s)*từ',sub_content_from)
	        if(temp_replace is not None):
	            temp_from_replace = re.search(r'(\“|\")(\s)*.+(\s)*(\”|\")',temp_replace.group())
	            from_replace = temp_from_replace.group()
	            temp_replace = re.search(r'(được\s)*(thay\s)*bằng\s(cụm\s)*từ\s(\“|\")(\s)*.+(\s)*(\”|\")',sub_content)
	            if(temp_replace is not None):
		            temp_to_replace = re.search(r'(\“|\")(\s)*.+(\s)*(\”|\")',temp_replace.group())
		            to_replace = temp_to_replace.group()
		            t = re.compile(r'(Đ|đ)iểm\s(\w{1,5}|\d{1,5})\s(k|K)hoản\s(\w{1,5}|\d{1,5})\s(Đ|đ)iều\s((\w{1,5})|(\d{1,5}))|(k|K)hoản\s(\w{1,5}|\d{1,5})\s(Đ|đ)iều\s((\w{1,5})|(\d{1,5}))|(đ|Đ)iều\s((\w{1,5})|(\d{1,5}))')
		            extract = t.finditer(sub_content,re.DOTALL)
		            if(lenIterator(extract)>0):
		                for extract in t.finditer(sub_content):
		                    temp_law = re.search(r'(đ|Đ)iều\s((\d{1,5})([a-zđ]|[A-Z])?)',sub_content[extract.span()[0]:extract.span()[1]])
		                    if(temp_law is not None):
		                        law = temp_law.group()
		                    else :
		                        law = None
		                    temp_item = re.search(r'(Khoản|khoản)\s(\w{1,5}|\d{1,5})',sub_content[extract.span()[0]:extract.span()[1]])
		                    if(temp_item is not None):
		                        item = temp_item.group()[8:]
		                    else :
		                        item = None
		                    temp_point = re.search(r'(đ|Đ)iểm\s(\w{1,5}|\d{1,5})',sub_content[extract.span()[0]:extract.span()[1]])
		                    if(temp_point is not None):
		                        point = temp_point.group()[8:]
		                    else :
		                        point = None
		                    yield[
		                        law_id,
			                    position,
								type_modify,
			                    None,
			                    None,
			                    None,
			                    law,
			                    item,
			                    point,
			                    sub_content,
			                    from_replace,
			                    to_replace,
			                    numerical_symbol,
			                    released_date
		                    ]
	        else :
	            yield[
	                law_id,
			        position,
					type_modify,
			        content,
			        None,
			        None,
			        None,
			        None,
			        None,
			        None,
			        None,
			        None,
			        numerical_symbol,
			        released_date
	            ]
	if(type_modify == 7):
	    text_delete = re.search(r'(\“|\").+(\”|\")',content,re.M|re.I)
	    if(text_delete is not None):
	        # numerical_symbol = get_numerical_symbol(content)
	        t = re.compile(r'(Đ|đ)iểm\s(\w{1,5}|\d{1,5})\s(k|K)hoản\s(\w{1,5}|\d{1,5})\s(Đ|đ)iều\s((\w{1,5})|(\d{1,5}))\s(c|C)hương\s(\w{1,10}|\d{1,5})\s|(k|K)hoản\s(\w{1,5}|\d{1,5})\s(Đ|đ)iều\s((\w{1,5})|(\d{1,5}))\s(c|C)hương\s(\w{1,10}|\d{1,5})\s|(Đ|đ)iều\s((\w{1,5})|(\d{1,5}))\s(c|C)hương\s(\w{1,10}|\d{1,5})\s|(c|C)hương\s(\w{1,10}|\d{1,5})\s|(Đ|đ)iểm\s(\w{1,5}|\d{1,5})\s(k|K)hoản\s(\w{1,5}|\d{1,5})\s(Đ|đ)iều\s((\w{1,5})|(\d{1,5}))|(k|K)hoản\s(\w{1,5}|\d{1,5})\s(Đ|đ)iều\s((\w{1,5})|(\d{1,5}))|(đ|Đ)iều\s((\w{1,5})|(\d{1,5}))')
	        extract = t.finditer(content)
	        if(lenIterator(extract)>0):
	            for extract in t.finditer(content):
	                temp_chapter = re.search(r'(c|C)hương\s(\w{1,10}|\d{1,5})',content[extract.span()[0]:extract.span()[1]])
	                if(temp_chapter is not None):
	                    chapter = temp_chapter.group()
	                else:
	                    chapter = None
	                temp_law = re.search(r'(đ|Đ)iều\s((\d{1,5})([a-zđ]|[A-Z])?)',content[extract.span()[0]:extract.span()[1]])
	                if(temp_law is not None):
	                    law = temp_law.group()
	                else :
	                    law = None
	                temp_item = re.search(r'(Khoản|khoản)\s(\w{1,5}|\d{1,5})',content[extract.span()[0]:extract.span()[1]])
	                if(temp_item is not None):
	                    item = temp_item.group()[8:]
	                else :
	                    item = None
	                temp_point = re.search(r'(đ|Đ)iểm\s(\w{1,5}|\d{1,5})',content[extract.span()[0]:extract.span()[1]])
	                if(temp_point is not None):
	                    point = temp_point.group()[8:]
	                else :
	                    point = None
	                yield[
	                    law_id,
	                    position,
						type_modify,
	                    None,
	                    chapter,
	                    None,
	                    law,
	                    item,
	                    point,
	                    text_delete.group(),
	                    None,
	                    None,
	                    numerical_symbol,
	                    released_date
	                ]
	    else :
	    	t = re.compile(r'(Đ|đ)iểm\s(\w{1,5}|\d{1,5})\s(k|K)hoản\s(\w{1,5}|\d{1,5})\s(Đ|đ)iều\s((\w{1,5})|(\d{1,5}))\s(c|C)hương\s(\w{1,10}|\d{1,5})\s|(k|K)hoản\s(\w{1,5}|\d{1,5})\s(Đ|đ)iều\s((\w{1,5})|(\d{1,5}))\s(c|C)hương\s(\w{1,10}|\d{1,5})\s|(Đ|đ)iều\s((\w{1,5})|(\d{1,5}))\s(c|C)hương\s(\w{1,10}|\d{1,5})\s|(c|C)hương\s(\w{1,10}|\d{1,5})\s|(Đ|đ)iểm\s(\w{1,5}|\d{1,5})\s(k|K)hoản\s(\w{1,5}|\d{1,5})\s(Đ|đ)iều\s((\w{1,5})|(\d{1,5}))|(k|K)hoản\s(\w{1,5}|\d{1,5})\s(Đ|đ)iều\s((\w{1,5})|(\d{1,5}))|(đ|Đ)iều\s((\w{1,5})|(\d{1,5}))')
	        extract = t.finditer(content)
	        if(lenIterator(extract)>0):
	            for extract in t.finditer(content):
	                temp_chapter = re.search(r'(c|C)hương\s(\w{1,10}|\d{1,5})',content[extract.span()[0]:extract.span()[1]])
	                if(temp_chapter is not None):
	                    chapter = temp_chapter.group()
	                else:
	                    chapter = None
	                temp_law = re.search(r'(đ|Đ)iều\s((\d{1,5})([a-zđ]|[A-Z])?)',content[extract.span()[0]:extract.span()[1]])
	                if(temp_law is not None):
	                    law = temp_law.group()
	                else :
	                    law = None
	                temp_item = re.search(r'(Khoản|khoản)\s(\w{1,5}|\d{1,5})',content[extract.span()[0]:extract.span()[1]])
	                if(temp_item is not None):
	                    item = temp_item.group()[8:]
	                else :
	                    item = None
	                temp_point = re.search(r'(đ|Đ)iểm\s(\w{1,5}|\d{1,5})',content[extract.span()[0]:extract.span()[1]])
	                if(temp_point is not None):
	                    point = temp_point.group()[8:]
	                else :
	                    point = None
	                yield[
	                    law_id,
	                    position,
						type_modify,
	                    None,
	                    chapter,
	                    None,
	                    law,
	                    item,
	                    point,
	                    "NA",
	                    None,
	                    None,
	                    numerical_symbol,
	                    released_date
	                ]
	        yield[
	            law_id,
		        position,
				type_modify,
		        None,
		        None,
		        None,
		        None,
		        None,
		        None,
		        None,
		        None,
		        None,
		        numerical_symbol,
		        released_date
	        ]
	if(type_modify == 5):
	    location = re.search('(t|T)ên của\s.*\sđược\s((s|S)ửa đổi\,\s)*((b|B)ổ sung\s)*',content)
	    if(location is not None):
	        sub_content = location.group()
	        text = re.search('(\"|\").*(\"|\")',content)
	        t = re.compile(r'(Đ|đ)iểm\s(\w{1,5}|\d{1,5})\s(k|K)hoản\s(\w{1,5}|\d{1,5})\s(Đ|đ)iều\s((\w{1,5})|(\d{1,5}))\s(c|C)hương\s(\w{1,10}|\d{1,5})\s|(k|K)hoản\s(\w{1,5}|\d{1,5})\s(Đ|đ)iều\s((\w{1,5})|(\d{1,5}))\s(c|C)hương\s(\w{1,10}|\d{1,5})\s|(Đ|đ)iều\s((\w{1,5})|(\d{1,5}))\s(c|C)hương\s(\w{1,10}|\d{1,5})\s|(c|C)hương\s(\w{1,10}|\d{1,5})\s|(Đ|đ)iểm\s(\w{1,5}|\d{1,5})\s(k|K)hoản\s(\w{1,5}|\d{1,5})\s(Đ|đ)iều\s((\w{1,5})|(\d{1,5}))|(k|K)hoản\s(\w{1,5}|\d{1,5})\s(Đ|đ)iều\s((\w{1,5})|(\d{1,5}))|(đ|Đ)iều\s((\w{1,5})|(\d{1,5}))')
	        extract = t.finditer(sub_content)
	        if(lenIterator(extract)>0):
	            for extract in t.finditer(sub_content):
	                temp_chapter = re.search(r'(c|C)hương\s(\w{1,10}|\d{1,5})',sub_content[extract.span()[0]:extract.span()[1]])
	                if(temp_chapter is not None):
	                    chapter = temp_chapter.group()
	                else:
	                    chapter = None
	                temp_law = re.search(r'(đ|Đ)iều\s((\d{1,5})([a-zđ]|[A-Z])?)',sub_content[extract.span()[0]:extract.span()[1]])
	                if(temp_law is not None):
	                    law = temp_law.group()
	                else :
	                    law = None
	                temp_item = re.search(r'(Khoản|khoản)\s(\w{1,5}|\d{1,5})',sub_content[extract.span()[0]:extract.span()[1]])
	                if(temp_item is not None):
	                    item = temp_item.group()[8:]
	                else :
	                    item = None
	                temp_point = re.search(r'(đ|Đ)iểm\s(\w{1,5}|\d{1,5})',sub_content[extract.span()[0]:extract.span()[1]])
	                if(temp_point is not None):
	                    point = temp_point.group()[8:]
	                else :
	                    point = None
	                yield[
	                        law_id,
		                    position,
							type_modify,
		                    None,
		                    chapter,
		                    None,
		                    law,
		                    item,
		                    point,
		                    sub_content,
		                    None,
		                    text.group(),
		                    numerical_symbol,
		                    released_date
	                ]
	    else :
	        yield[
	            law_id,
	            position,
				type_modify,
	            None,
	            None,
	            None,
	            None,
	            None,
	            None,
	            None,
	            None,
	            None,
	            numerical_symbol,
	            released_date
	        ]
	if(type_modify == 6):
	    text = re.search('(\“|\"|\").*(\”|\"|\")',content)
	    if(text is not None):
	        t = re.compile(r'(Đ|đ)iểm\s(\w{1,5}|\d{1,5})\s(k|K)hoản\s(\w{1,5}|\d{1,5})\s(Đ|đ)iều\s((\w{1,5})|(\d{1,5}))\s(c|C)hương\s(\w{1,10}|\d{1,5})\s|(k|K)hoản\s(\w{1,5}|\d{1,5})\s(Đ|đ)iều\s((\w{1,5})|(\d{1,5}))\s(c|C)hương\s(\w{1,10}|\d{1,5})\s|(Đ|đ)iều\s((\w{1,5})|(\d{1,5}))\s(c|C)hương\s(\w{1,10}|\d{1,5})\s|(c|C)hương\s(\w{1,10}|\d{1,5})\s|(Đ|đ)iểm\s(\w{1,5}|\d{1,5})\s(k|K)hoản\s(\w{1,5}|\d{1,5})\s(Đ|đ)iều\s((\w{1,5})|(\d{1,5}))|(k|K)hoản\s(\w{1,5}|\d{1,5})\s(Đ|đ)iều\s((\w{1,5})|(\d{1,5}))|(đ|Đ)iều\s((\w{1,5})|(\d{1,5}))')
	        extract = t.finditer(content)
	        if(lenIterator(extract)>0):
	            for extract in t.finditer(content):
	                temp_chapter = re.search(r'(c|C)hương\s(\w{1,10}|\d{1,5})',content[extract.span()[0]:extract.span()[1]])
	                if(temp_chapter is not None):
	                    chapter = temp_chapter.group()
	                else:
	                    chapter = None
	                temp_law = re.search(r'(đ|Đ)iều\s((\d{1,5})([a-zđ]|[A-Z])?)',content[extract.span()[0]:extract.span()[1]])
	                if(temp_law is not None):
	                    law = temp_law.group()
	                else :
	                    law = None
	                temp_item = re.search(r'(Khoản|khoản)\s(\w{1,5}|\d{1,5})',content[extract.span()[0]:extract.span()[1]])
	                if(temp_item is not None):
	                    item = temp_item.group()[8:]
	                else :
	                    item = None
	                temp_point = re.search(r'(đ|Đ)iểm\s(\w{1,5}|\d{1,5})',content[extract.span()[0]:extract.span()[1]])
	                if(temp_point is not None):
	                    point = temp_point.group()[8:]
	                else :
	                    point = None
	                yield[
	                    law_id,
	                    position,
						type_modify,
	                    None,
	                    chapter,
	                    None,
	                    law,
	                    item,
	                    point,
	                    None,
	                    None,
	                    text.group(),
	                    numerical_symbol,
	                    released_date
	                ]
	    else :
	        yield[
	            law_id,
		        position,
				type_modify,
		        None,
		        None,
		        None,
		        None,
		        None,
		        None,
		        None,
		        None,
		        None,
		        numerical_symbol,
		        released_date
	        ]
