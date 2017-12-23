import sys
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
		
		token = {"word":word, "normal_form": normal_form, "pos": pos, "tags": tags.split("|")}
		ud_tree.append(token)

	return (ud_tree)

def convert_token_to_apertium(token):
	result_token = "^%s/%s" % (token["word"], token["normal_form"])

	result_token += ud2apr[token["pos"]]

	for tag in token["tags"]:
		result_token += ud2apr[tag]
	
	result_token += "$"

	result_token = result_token.replace("<>", "")
	return result_token

if __name__ == "__main__":
	tags_file = codecs.open(sys.argv[1], "r", "utf-8")
	input_file = codecs.open(sys.argv[2], "r", "utf-8")
	output_file = codecs.open(sys.argv[3], "w", "utf-8")

	ud2apr = get_tags(tags_file)
	ud_tree = parse_ud(input_file)

	for token in ud_tree:
		ap_token = convert_token_to_apertium(token)
		print(ap_token)
		output_file.write(ap_token+"\n")

	tags_file.close()
	input_file.close()
	output_file.close()