import os
import point


class codegen:
    def __init__(self, filename, nodename, miniblocks):
        self.filename = filename
        self.nodename = nodename
        self.miniblocks = miniblocks
        self.scaling = 16.0

    def writeToFile(self, export_as):
        s = self.scaling
        output_file = open(export_as, "w+")
        output_file.write("-- Generated code\n\n")
        output_file.write("minetest.register_node(\"modename:nodename\", {\n")
        output_file.write("\tdrawtype = \"nodebox\",\n")
        output_file.write("\tparamtype = \"light\",\n")
        output_file.write("\tnode_box = {\n")
        output_file.write("\t\ttype = \"fixed\",\n")
        output_file.write("\t\tfixed = {\n")
        for b in self.miniblocks:
            output_file.write("\t\t\t{" + ", ".join([str(b.p1.x/s), str(b.p1.y/s), str(b.p1.z/s),
                             str(b.p2.x/s), str(b.p2.y/s), str(b.p2.z/s)]) + "},\n")
        output_file.write("\t\t}\n\t},")
        output_file.write("\tgroups={oddly_breakable_by_hand=2}\n})")

        output_file.close()
