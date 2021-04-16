# coding: utf8

#refrence from:https://github.com/zgzczzw/LinkMapParser, thanks
#edit: yooongs

import sys
import os

unit = "kb"

#system file name list filter
system_file_name_List = ["linker synthesized", ".tbd", ".ios.a"]
#get total size, other than this files
other_than_files = []

def read_base_link_map_file(base_link_map_file, base_link_map_result_file):
    try:
        link_map_file = open(base_link_map_file)
    except IOError:
        print "Read file " + base_link_map_file + " failed!"
        return
    else:
        try:
            content = link_map_file.read()
        except IOError:
            print "Read file " + base_link_map_file + " failed!"
            return
        else:
            obj_file_tag_index = content.find("# Object files:")
            sub_obj_file_symbol_str = content[obj_file_tag_index + 15:]
            symbols_index = sub_obj_file_symbol_str.find("# Symbols:")
            if obj_file_tag_index == -1 or symbols_index == -1 or content.find("# Path:") == -1:
                print "The Content of File " + base_link_map_file + " is Invalid."
                pass
            link_map_file_tmp = open(base_link_map_file)
            reach_files = 0
            reach_sections = 0
            reach_symbols = 0
            size_map = {}
            while 1:
                line = link_map_file_tmp.readline()
                if not line:
                    break
                if line.startswith("#"):
                    if line.startswith("# Object files:"):
                        reach_files = 1
                        pass
                    if line.startswith("# Sections"):
                        reach_sections = 1
                        pass
                    if line.startswith("# Symbols"):
                        reach_symbols = 1
                        pass
                    pass
                else:
                    if reach_files == 1 and reach_sections == 0 and reach_symbols == 0:
                        index = line.find("]")
                        if index != -1:
                            symbol = {"file": line[index + 2:-1]}
                            key = int(line[1: index])
                            size_map[key] = symbol
                        pass
                    elif reach_files == 1 and reach_sections == 1 and reach_symbols == 0:
                        pass
                    elif reach_files == 1 and reach_sections == 1 and reach_symbols == 1:
                        symbols_array = line.split("\t")
                        if len(symbols_array) == 3:
                            file_key_and_name = symbols_array[2]
                            size = int(symbols_array[1], 16)
                            index = file_key_and_name.find("]")
                            if index != -1:
                                key = file_key_and_name[1:index]
                                key = int(key)
                                symbol = size_map[key]
                                if symbol:
                                    if "size" in symbol:
                                        symbol["size"] += size
                                        pass
                                    else:
                                        symbol["size"] = size
                                    pass
                                pass
                            pass
                        pass
                    else:
                        print "Invalid #3"
                        pass
            total_size  = 0
            other_than_size = 0
            a_file_map = {}
            for key in size_map:
                symbol = size_map[key]
                if "size" in symbol:
                    o_file_name = symbol["file"].split("/")[-1]
                    a_file_name = o_file_name.split("(")[0]

                    #system symbol filter
                    isSystemFile = False
                    for name in system_file_name_List:
                        if name in a_file_name:
                            isSystemFile = True
                            break
                    if isSystemFile:
                        continue

                    total_size += symbol["size"]
                    other_than_size += symbol["size"]

                    for otf in other_than_files:
                        if otf in a_file_name:
                            other_than_size -= symbol["size"]
                            break

                    if a_file_name in a_file_map:
                        a_file_map[a_file_name] += symbol["size"]
                        pass
                    else:
                        a_file_map[a_file_name] = symbol["size"]
                        pass
                    pass
                else:
                    print "WARN : some error occurred for key ",
                    print key

            a_file_sorted_list = sorted(a_file_map.items(), key=lambda x: x[1], reverse=True)

            print "%s" % "=".ljust(80, '=')
            print "%s" % (base_link_map_file+" each size of Object files").center(87)
            print "%s" % "=".ljust(80, '=')

            if os.path.exists(base_link_map_result_file):
                os.remove(base_link_map_result_file)
                pass
            print "Creating Result File : %s" % base_link_map_result_file
            output_file = open(base_link_map_result_file, "w")
            for item in a_file_sorted_list:
                print "%s%.4f%s" % (item[0].ljust(50), get_with_unit(item[1]), unit)
                output_file.write("%s \t\t\t%.4f%s\n" % (item[0].ljust(50), get_with_unit(item[1]), unit))
                pass
            print "%s%.4f%s" % ("total size:".ljust(50), get_with_unit(total_size), unit)
            print "\n"
            if len(other_than_files) > 0:
                otfiles = ",".join(str(x) for x in other_than_files)
                print "%s%.4f%s" % ("other than [" + otfiles + "], total size:", get_with_unit(other_than_size), unit)
            output_file.write("%s%.4f%s" % ("total size:".ljust(50), get_with_unit(total_size), unit))
            link_map_file_tmp.close()
            output_file.close()
        finally:
            link_map_file.close()

def get_with_unit(value):
    it = value
    if unit == "kb":
        it = value/1024.0
    elif unit == "mb":
        it = value/1024.0/1024.0
    return it


def parse_result_file(result_file_name):
    base_bundle_list = []
    result_file = open(result_file_name)
    while 1:
        line = result_file.readline()
        if not line:
            break
        bundle_and_size = line.split()
        if len(bundle_and_size) == 2 and line.find(":") == -1:
            bundle_and_size_map = {"name": bundle_and_size[0], "size": bundle_and_size[1]}
            base_bundle_list += [bundle_and_size_map]
            pass
    return base_bundle_list


def compare(base_bundle_list, target_bundle_list):
    print "%s" % "=".ljust(80, '=')
    print "%s" % "compare result".center(84)
    print "%s" % "=".ljust(80, '=')
    print "%s%s%s%s" % ("Object files".ljust(54), "base line".ljust(14), "target".ljust(14), "add+/delete-".ljust(14))

    target_maps = {}
    for target_map in target_bundle_list:
        target_maps[target_map["name"]] = float(target_map["size"].split(unit)[0])
    base_maps = {}
    for base_map in base_bundle_list:
        base_maps[base_map["name"]] = float(base_map["size"].split(unit)[0])

    samekeys = list(set(target_maps.keys()).intersection(set(base_maps.keys())))
    for name in samekeys:
        base_size_value = base_maps[name]
        target_size_value = target_maps[name]
        if base_size_value != target_size_value:
            print "%s%s%s%.4f" % (name.ljust(54), str("%.4f%s" % (base_size_value, unit)).ljust(14),
                                  str("%.4f%s" % (target_size_value, unit)).ljust(14),
                                  (target_size_value - base_size_value))
    addkeys = list(set(target_maps.keys()).difference(set(base_maps.keys())))
    for name in addkeys:
        base_size_value = 0.0
        target_size_value = target_maps[name]
        print "%s%s%s%s" % (name.ljust(54), str("%.4f%s" % (base_size_value, unit)).ljust(14),
                            str("%.4f%s" % (target_size_value, unit)).ljust(14),
                            "+".center(12))
    deletekeys = list(set(base_maps.keys()).difference(set(target_maps.keys())))
    for name in deletekeys:
        base_size_value = base_maps[name]
        target_size_value = 0.0
        print "%s%s%s%s" % (name.ljust(54), str("%.4f%s" % (base_size_value, unit)).ljust(14),
                              str("%.4f%s" % (target_size_value, unit)).ljust(14),
                              "-".center(12))

def print_help():
    print "%s" % "=".ljust(80, '=')
    print "%s%s\n" % ("".ljust(10), "Link Map parse tools".ljust(80))
    print "%s%s\n" % ("".ljust(10), "- Usage : python parselinkmap.py arg1 <arg2>".ljust(80))
    print "%s%s" % ("".ljust(10), "- arg1 ：path of link map file(base line)".ljust(80))
    print "%s%s\n" % ("".ljust(10), "- arg2 ：path of link map file(compare)".ljust(80))
    print "%s%s" % ("".ljust(10), "tips: can intput only arg1".ljust(80))
    print "%s" % "=".ljust(80, '=')


def clean_result_file(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)
        pass


def main():
    if len(sys.argv) == 2:
        need_compare = 0
        pass
    elif len(sys.argv) == 3:
        need_compare = 1
        pass
    else:
        print_help()
        return
        pass

    base_map_link_file = sys.argv[1]
    output_file_path = os.path.dirname(base_map_link_file)
    if output_file_path:
        base_output_file = output_file_path + "/BaseLinkMapResult.txt"
        pass
    else:
        base_output_file = "BaseLinkMapResult.txt"
        pass
    read_base_link_map_file(base_map_link_file, base_output_file)

    if need_compare == 1:
        target_map_link_file = sys.argv[2]
        output_file_path = os.path.dirname(target_map_link_file)
        if output_file_path:
            target_output_file = output_file_path + "/TargetLinkMapResult.txt"
            pass
        else:
            target_output_file = "TargetLinkMapResult.txt"
            pass
        read_base_link_map_file(target_map_link_file, target_output_file)

        base_bundle_list = parse_result_file(base_output_file)
        target_bundle_list = parse_result_file(target_output_file)

        compare(base_bundle_list, target_bundle_list)


if __name__ == "__main__":
    unit = raw_input("intput unit(mb/kb):")
    if (unit != "mb") & (unit != "kb"):
        print "Invalid unit! please intput mb or kb!"
        exit()
    main()
