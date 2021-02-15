def circuit_to_tikz_string(circuit, size):

    line_protrusion = 0.5
    gate_distance = 1
    drawing_offset = 0

    dot_radius = 0.1
    circle_radius = 0.2

    tikz_string = '';

    circuit_len = len(circuit) - 1

    line_start = drawing_offset - line_protrusion
    line_end = circuit_len + line_protrusion

    for qbit in range(1, size + 1):

        tikz_string = f"{tikz_string}\draw[thick] ({line_start},{-qbit}) node[anchor=east] {{Input {qbit}}} -- ({line_end},{-qbit}) node[anchor=west] {{Output {qbit}}};\n"

    gate_position = drawing_offset
    for gate in circuit:

        tikz_string = f"{tikz_string}\\filldraw ({gate_position},{-gate[0]}) circle ({dot_radius});\n"
        tikz_string = f"{tikz_string}\\draw[thick] ({gate_position},{-gate[1]}) circle ({circle_radius});\n"

        connection_upper = -gate[0] - dot_radius
        connection_lower = -gate[1] - circle_radius
        if (gate[0] > gate[1]):
            connection_upper = -gate[1] + circle_radius
            connection_lower = -gate[0] + dot_radius

        tikz_string = f"{tikz_string}\\draw[thick] ({gate_position},{connection_upper}) -- ({gate_position},{connection_lower});\n"

        gate_position += gate_distance

    return tikz_string


def circuit_to_tikz_file(size, circuit, file_name):

    tikz_picture_string = f"\\begin{{tikzpicture}}\n{circuit_to_tikz_string(size, circuit)}\\end{{tikzpicture}}\n"

    tikz_file_name = file_name + ".tikz"

    file = open(tikz_file_name, "w")
    file.write(tikz_picture_string)
    file.close()

    return tikz_picture_string

#size = 6
#circuit = [(5,4),(2,1),(4,2),(6,3),(5,3),(5,4),(6,5),(3,4),(4,3),(4,6),(3,5),(2,3),(1,2),(1,5),(1,4)]

#tikz = circuit_to_tikz_string(circuit, size)

#print(tikz)


