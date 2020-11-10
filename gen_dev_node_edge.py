import json
import itertools

def main():
    src_path = "outputs/app_info.json"
    src_file = open(src_path, 'r')
    src_json = json.load(src_file)

    node_out_path = "outputs/dev_nodes.csv"
    node_out = open(node_out_path, 'w', encoding="utf-8")
    node_out.write("Id; Label; type\n")

    developer_list = []
    publisher_list = []
    relationship_list = []
    for app_id in src_json:
        app = src_json[app_id]
        # exclude unsuccessful parsing
        if "success" in app:
            if not app["success"]:
                continue
        # exclude non-games
        if app["data"]["type"] == "game":
            if "developers" in app["data"]:
                dev_list = app["data"]["developers"]
                pub_list = app["data"]["publishers"]
                for i in range(len(dev_list)):
                    dev_list[i] = dev_list[i].strip()
                for i in range(len(pub_list)):
                    pub_list[i] = pub_list[i].strip()
                developer_list += dev_list
                publisher_list += pub_list
                pairs = itertools.combinations(list(set(dev_list + pub_list)), 2)
                for pair in pairs:
                    if pair and (pair not in relationship_list) and pair[0] and pair[1]:
                        relationship_list.append(pair)
    developer_list = list(set(developer_list))
    publisher_list = list(set(publisher_list))
    both_list = []
    for dev in developer_list:
        if ";" in dev:
            if '"' in dev:
                dev = "'" + dev + "'"
            else:
                dev = '"' + dev + '"'
        if dev in publisher_list:
            both_list.append(dev)
        else:
            node_out.write(dev + "; " + dev + "; developer\n")
    for pub in publisher_list:
        if ";" in pub:
            if '"' in pub:
                pub = "'" + pub + "'"
            else:
                pub = '"' + pub + '"'
        if pub not in both_list:
            node_out.write(pub + "; " + pub + "; publisher\n")
    for both in both_list:
        node_out.write(both + "; " + both + "; both\n")
    node_out.close()

    edge_out_path = "outputs/dev_edges.csv"
    edge_out = open(edge_out_path, 'w', encoding="utf-8")
    edge_out.write("Source; Target\n")
    for relationship in relationship_list:
        source = relationship[0]
        if ";" in source:
            source = '"' + source + '"'
        target = relationship[1]
        if ";" in target:
            target = '"' + target + '"'
        edge_out.write(source + "; " + target + "\n")
    edge_out.close()


main()