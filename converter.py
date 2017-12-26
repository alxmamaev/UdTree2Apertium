import sys
import re
import codecs

ud2apr = None

def get_tags(tags_file):
	tags = {}
	while True:
		line = tags_file.readline()
		if not line: break

		ud_tag, ap_tag = line.strip().split(",")
		tags[ud_tag] = ap_tag

	return tags

def parse_ud(input_file):
	ud_tree = []
	while True:
		line = input_file.readline()
		if not line: break
		if line[0] == "#" or not line.strip(): continue

		_, word, normal_form, pos, _, tags, _, _, _, _ = line.strip().split("\t")
		

		reult_tags = []
		for t in tags.split("|") + [pos]:
			tag = ud2apr.get(t)
			if tag is None: continue
	
			reult_tags += re.findall("\<[a-z]*\>", tag)

		token = {"word":word, "normal_form": normal_form, "pos": pos, "tags": set(reult_tags)}
		ud_tree.append(token)

	return (ud_tree)

def get_apertium_tags(input_file):
	result_tags = {}

	while True:
		line = input_file.readline()
		if line.startswith("#"): continue
		if not line:break
		
		word = line.split("\t")[1:2]
		
		if not word: continue

		word = word[0]

		word = word[1:-1]
		tokens = word.split("/")

		if tokens[0] in result_tags:
			continue

		variants_of_words = []
		for token in tokens[1:]:
			normal_form = token.split("<")[0]
			tags = re.findall("\<[a-z]*\>", token)
			
			variants_of_words.append({"normal_form":normal_form, "tags":tags})
	
		result_tags[tokens[0].lower()] = variants_of_words
	return result_tags

def convert_token_to_apertium(token, apertium_parse_result):
	result_token = "^%s/" % (token["word"])

	if token["word"] == "-":
		index_word = "-"
	else:
		index_word = token["word"].lower().split("-")[0]

	if not index_word in apertium_parse_result:
		return None

	max_intersection = 0
	analysis = set()
	
	for variant in apertium_parse_result[index_word]:
		tags = "".join(variant["tags"])
		normal_from = variant["normal_form"]

		analys = normal_from+tags
		intersection_len = len(set(variant["tags"]) & token["tags"])

		if  intersection_len > max_intersection:
			max_intersection = intersection_len
			analysis = {analys}

		if intersection_len == max_intersection:
			analysis.add(analys)

	result_token += "/".join(list(analysis))
	result_token += "$"

	result_token = result_token.replace("<>", "")
	return result_token

if __name__ == "__main__":
	tags_file = codecs.open(sys.argv[1], "r", "utf-8")
	apertium_file = codecs.open(sys.argv[2], "r", "utf-8")
	input_file = codecs.open(sys.argv[3], "r", "utf-8")
	output_file = codecs.open(sys.argv[4], "w", "utf-8")

	ud2apr = get_tags(tags_file)
	ud_tree = parse_ud(input_file)
	apertium_parse_result = get_apertium_tags(apertium_file)


	for token in ud_tree:
		ap_token = convert_token_to_apertium(token, apertium_parse_result)
		
		if ap_token is None:
			continue
		
		print(ap_token)
		output_file.write(ap_token+"\n")

	apertium_file.close()
	tags_file.close()
	input_file.close()
	output_file.close()