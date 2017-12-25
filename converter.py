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
		
		token = {"word":word, "normal_form": normal_form, "pos": pos, "tags": set([ud2apr[t] for t in tags.split("|") + [pos]])}
		ud_tree.append(token)

	return (ud_tree)

def get_apertium_tags(input_file):
	result_tags = {}
	while True:
		line = input_file.readline()
		if not line: break
		if not line.startswith("# text = "): continue

		line = line.replace("# text = ", "")
		words = line.replace("$ ", "$").replace("^", "").strip().split("$")[:-1]
		# import pdb;pdb.set_trace()
		for word in words:
			tokens = word.split("/")
			
			if tokens[0] in result_tags:
				continue

			variants_of_words = []
			for token in tokens[1:]:
				normal_form = token.split("<")[0]
				
				tags = re.findall("\<[a-z]*\>", token)
			
				variants_of_words.append({"normal_form":normal_form, "tags":tags})
			
			result_tags[tokens[0]] = variants_of_words

	return result_tags

def convert_token_to_apertium(token, apertium_parse_result):
	result_token = "^%s/" % (token["word"])

	max_intersection = 0
	result_tags = []
	for variant in apertium_parse_result[token["word"]]:
		if variant["normal_form"] != token["normal_form"]:
			continue

		if len(set(variant["tags"]) & token["tags"]) > max_intersection:
			max_intersection = len(set(variant["tags"]) & token["tags"])
			result_tags = variant["tags"]

	result_token += token["normal_form"]
	result_token += "".join(result_tags)
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
		print(ap_token)
		output_file.write(ap_token+"\n")

	apertium_file.close()
	tags_file.close()
	input_file.close()
	output_file.close()