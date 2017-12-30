import sys
import re
import codecs

ud2apr = None


# function to load csv tags dict
def load_tags_dict(tags_file):
	tags = {}
	while True:
		line = tags_file.readline()
		if not line: break

		ud_tag, apr_tag = line.strip().split(",")
		tags[ud_tag] = apr_tag

	return tags

def convert_token_from_ud_to_apertium(token, word2analys):
	result_token = "^%s/" % (token["word"])

	if token["word"] == "-":
		index_word = "-"
	else:
		index_word = token["word"].lower().split("-")[0]

	if not index_word or not index_word in word2analys:
		return None

	max_intersection = 0
	word_analysis = set()
	
	for analys in word2analys[index_word]:
		analys = normal_from+tags
		tags = set(re.findall("\<[a-z]*\>", analys)) 

		intersection_len = len(tags & token["tags"])

		if  intersection_len > max_intersection:
			max_intersection = intersection_len
			word_analysis = {analys}

		elif intersection_len == max_intersection:
			word_analysis.add(analys)

	result_analys = "/".join(list(word_analysis))

	if not result_analys:
		return None

	result_token += result_analys
	result_token += "$"

	result_token = result_token.replace("<>", "")
	return result_token



def get_ud_token(ud_tree_file):
	while True:
		line = ud_tree_file.readline()
		
		if not line: return None
		if line.startswith("#") or not line.strip(): continue

		_, word, normal_form, pos, _, tags, _, _, _, _ = line.strip().split("\t")
		break

	word_tags = set()
	for tag in tags.split("|") + [pos]:
		tag = ud2apr.get(tag)
		if tag is None: continue

		word_tags = word_tags | set(re.findall("\<[a-z]*\>", tag)) 

	token = {"word": word, "tags":word_tags}

	return token


def get_aprtium_token(ud_tree_file):
	while True:
		line = ud_tree_file.readline()
		
		if not line: return None
		if not line.strip(): continue
		if not re.findall("\^.*\$", line): return -1

		line = line[1:-2]
		word, variants_of_parsing = line.split("/")[0], set(line.split("/")[1:]) 
		break

	token = {"word": word, "variants_of_parsing":variants_of_parsing}

	return token

def get_next_token(apertium_file, ud_tree_file):
	apertium_token  = get_aprtium_token(apertium_file)
	ud_token = get_ud_token(ud_tree_file)

	if apertium_token == -1:
		return ""

	if apertium_token is None or ud_token is None:
		return None

	token = "^%s/" % apertium_token["word"]

	max_intersection = 0
	variants_of_parsing = []
	for variant in apertium_token["variants_of_parsing"]:
		tags = set(re.findall("\<[a-z]*\>", variant))
		intersection = len(ud_token["tags"] & tags)

		if max_intersection == intersection:
			variants_of_parsing.append(variant)
		elif max_intersection < intersection:
			max_intersection = intersection
			variants_of_parsing = [variant]

	token += "/".join(variants_of_parsing)
	token += "$"
	return token


if __name__ == "__main__":
	tags_file = codecs.open(sys.argv[1], "r", "utf-8")
	apertium_file = codecs.open(sys.argv[2], "r", "utf-8")
	ud_tree_file = codecs.open(sys.argv[3], "r", "utf-8")
	output_file = codecs.open(sys.argv[4], "w", "utf-8")

	ud2apr = load_tags_dict(tags_file)

	while True:
		token = get_next_token(apertium_file, ud_tree_file)

		if token is None:
			break

		print(token)
		output_file.write(token+"\n")

	apertium_file.close()
	tags_file.close()
	ud_tree_file.close()
	output_file.close()