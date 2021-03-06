import os


class codegen:
    def __init__(self, filename, nodename, blocks, resolution):
        self.filename = filename
        self.nodename = nodename
        self.blocks = blocks
        self.scaling = resolution
        self.head = [
            "-- Generated code\n\n",
            "minetest.register_node(\"yourmode:yournode\", {\n",
            "\ttiles = {\n",
            "\t\t\"picture.png\",\n",
            "\t\t\"picture.png\",\n",
            "\t\t\"picture.png\",\n",
            "\t\t\"picture.png\",\n",
            "\t\t\"picture.png\",\n",
            "\t\t\"picture.png\",\n",
            "\t},\n",
            "\tdrawtype = \"nodebox\",\n",
            "\tnode_box = {\n",
            "\t\ttype=\"fixed\",\n",
            "\t\tfixed={\n"
        ]
        self.tail = [
       	    "\t\t}\n",
            "\t},\n",
            "\tgroups={oddly_breakable_by_hand=3}\n",
            "})\n"
        ]

    def writeToFile(self, export_as):
        s = self.scaling
        print(s)
        output_file = open(export_as, "w+")
        for line in self.head:
            output_file.write(line)
        for b in self.blocks:
            output_file.write("\t\t\t{" + ", ".join([
                str(b.p1()[0]/s), str(b.p1()[2]/s), str(b.p1()[1]/s),
                str(b.p2()[0]/s), str(b.p2()[2]/s), str(b.p2()[1]/s)]) + "},\n")
        for line in self.tail:
            output_file.write(line)
        output_file.close()

