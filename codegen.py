import os
import point


class codegen:
    def __init__(self, filename, nodename, miniblocks):
        self.filename = filename
        self.nodename = nodename
        self.miniblocks = miniblocks
        self.scaling = 16.0
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
	    "\tparamtype = \"light\",\n",
	    "\tnode_box = {\n",
	    "\t\ttype=\"fixed\",\n",
            "\t\tfixed={\n"
                ]
        self.tail = [
		"\t\t}\n",
                "\t},\n",
                "\tgroups={oddly_breakable_by_hand=2}\n",
                "})\n"
                ]


    def writeToFile(self, export_as):
        s = self.scaling
        output_file = open(export_as, "w+")
        for line in self.head:
            output_file.write(line)
        for b in self.miniblocks:
            output_file.write("\t\t\t{" + ", ".join([str(b.p1.x/s), str(b.p1.z/s), str(b.p1.y/s),
                             str(b.p2.x/s), str(b.p2.z/s), str(b.p2.y/s)]) + "},\n")
        for line in self.tail:
            output_file.write(line)
        output_file.close()

    def saveToFile(self, save_as):
        output_file = open(save_as, "w+")
        for b in self.miniblocks:
            output_file.write(" ".join([str(b.p1.x), str(b.p1.z), str(b.p1.y),
                             str(b.p2.x), str(b.p2.z), str(b.p2.y)]) + "\n")
        output_file.close()

    def loadFromFile(self, load_from):
        return
