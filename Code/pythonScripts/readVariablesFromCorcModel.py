import xml.etree.ElementTree as ET


def find_node_by_id(root, node_id_to_find):
    for node in root.iter():
        if node.attrib.get("id") == node_id_to_find:
            return node
    return None


def parse_java_variables(root, namespace):
    java_variables_dict = {}
    java_variables_node = root.find(".//cbcmodel:JavaVariables", namespaces=namespace)
    # TODO: read "variable"-children from found node
    if java_variables_node is not None:
        # print("\nJava Variables node found:")
        # ET.dump(java_variables_node)

        # Task 1: Parse and print Java Variables
        java_variables_dict = {}
        for variable_node in java_variables_node.findall(
            ".//variables", namespaces=namespace
        ):
            variable_name = variable_node.attrib.get("name")
            if variable_name:
                datatype, variable = variable_name.split()
                java_variables_dict[variable] = datatype
    else:
        print("\nJava Variables node not found.")
    return java_variables_dict


def parse_modifiables_list(root, node_id_to_find, namespace):
    modifiables_list = []
    found_node = find_node_by_id(root, node_id_to_find)
    if found_node is not None:
        # print(f"Node with ID '{node_id_to_find}' found:")
        # ET.dump(found_node)
        post_condition_node = found_node.find(".//postCondition", namespaces=namespace)
        if post_condition_node is not None:
            for modifiable_node in post_condition_node.findall(
                ".//modifiables", namespaces=namespace
            ):
                variable_name = modifiable_node.text
                modifiables_list.append(variable_name)
        else:
            print(f"Node with ID '{node_id_to_find}' has no postCondition-child.")
    else:
        print(f"Node with ID '{node_id_to_find}' not found.")

    return modifiables_list


def generate_triples(java_variables_dict, modifiables_list):
    triples_list = []
    for variable_name, datatype in java_variables_dict.items():
        found_as_modifiable = variable_name in modifiables_list
        triples_list.append((variable_name, found_as_modifiable, datatype))
    return triples_list


def read_vars_from_corc_model(file_path, node_id_to_find):
    # Load the file, read the content, and parse it into an XML tree
    tree = ET.parse(file_path)
    root = tree.getroot()
    # ET.dump(root)

    namespace = {"cbcmodel": "http://www.example.org/cbcmodel"}

    modifiables_list = parse_modifiables_list(root, node_id_to_find, namespace)
    # print("\nModifiables List:")
    # print(modifiables_list)

    java_variables_dict = parse_java_variables(root, namespace)
    # print("\nJava Variables Dictionary:")
    # print(java_variables_dict)

    triples_list = generate_triples(java_variables_dict, modifiables_list)
    # print("\nTriples List:")
    # print(triples_list)
    return triples_list


if __name__ == "__main__":
    file_path_param = (
        ".\\..\\..\\ExampleProblemDefinitions\\xPlusOne\\newDiagram.cbcmodel"
    )
    id_param = "4057a6e8-c7a5-4d44-82df-8f3b3d459ccd"

    read_vars_from_corc_model(file_path_param, id_param)
