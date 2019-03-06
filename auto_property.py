import os
import re
import argparse



def code_create(path, is_swagger, is_wiki):
    if is_swagger is True:
        code_create_swagger(path)
    elif is_wiki is True:
        code_create_wiki(path)
    else:
        code_create_json_dict(path)

def code_create_swagger(path):
    # 获取文件数据
    data = open(path, "r", encoding="utf-8", errors="ignore")

    # 读取第一行
    each = data.readline()

    # 属性列表
    my_property_name_list = list()
    my_property_annotation_list = list()
    # 存储文件原内容
    whole_string = ''

    while each:
        whole_string += each

        if each.find("@interface") != -1:
            each = data.readline()
            continue

        # (ex:hit (integer, optional): 0 未命中，1 命中) 类型默认为 NSString *
        if each.find(":") != -1:
            left = each.split(":")[0]
            right = each.split(":")[1]

            result = re.search(r"\b[a-zA-Z_0-9]+\b", left)
            if result != None:
                name = result.group(0)
                name = name.strip()
                my_property_name_list.append(name)
                my_property_annotation_list.append("///" + right)

                each = data.readline()
                continue


        # 都没匹配上则下一行继续
        each = data.readline()
        continue

    # 开始拼接
    property_string = ''
    for i in range(len(my_property_name_list)):
        each_property = my_property_name_list[i]
        each_property = "@property (nonatomic, copy) NSString *%s;\n" % (each_property)
        each_annotation = my_property_annotation_list[i]

        property_string += each_annotation
        property_string += each_property
        property_string += "\n"

    whole_string = whole_string.replace("@end", property_string)
    whole_string += "\n@end"

    with open(path, 'w', encoding='utf-8', errors='ignore') as f:
        f.write(whole_string)


def code_create_wiki(path):
    # 获取文件数据
    data = open(path, "r", encoding="utf-8", errors="ignore")

    # 读取第一行
    each = data.readline()

    # 属性列表
    my_property_name_list = list()
    my_property_annotation_list = list()
    # 存储文件原内容
    whole_string = ''

    while each:
        whole_string += each
        # (each example: otherRank     其它排名     array) 类型默认为 NSString *
        each = each.strip()
        res = re.match(r"^[a-zA-Z].*?", each)
        if res != None and each.find("     ") != -1:
            name = each.split("     ")[0].strip()
            right = each.split("     ")[1].strip()

            my_property_name_list.append(name)
            my_property_annotation_list.append("///" + right)

            each = data.readline()
            continue

        # 都没匹配上则下一行继续
        each = data.readline()
        continue

    # 开始拼接
    property_string = ''
    for i in range(len(my_property_name_list)):
        each_property = my_property_name_list[i]
        each_property = "@property (nonatomic, copy) NSString *%s;\n" % (each_property)
        each_annotation = my_property_annotation_list[i]

        property_string += each_annotation
        property_string += "\n"
        property_string += each_property
        property_string += "\n"

    whole_string = whole_string.replace("@end", property_string)
    whole_string += "@end"

    with open(path, 'w', encoding='utf-8', errors='ignore') as f:
        f.write(whole_string)


def code_create_json_dict(path):
    # 获取文件数据
    data = open(path, "r", encoding="utf-8", errors="ignore")

    # 读取第一行
    each = data.readline()

    # 属性列表
    my_property_name_list = list()

    # 存储文件原内容
    whole_string = ''

    while each:
        whole_string += each

        if each.find("import") != -1:
            each = data.readline()
            continue

        # 这个if针对dict格式 (ex:matchTime = 1542713700000) 类型默认为 NSString *
        if each.find("=") != -1:
            name = each.split("=")[0]
            name = name.strip()
            my_property_name_list.append(name)
            each = data.readline()
            continue

        # 这个if针对json格式 (ex: "teamName": "利物浦")
        match = re.findall('"(.*?)"', each)
        if len(match) > 0:
            name = match[0]
            my_property_name_list.append(name)
            each = data.readline()
            continue

        # 都没匹配上则下一行继续
        each = data.readline()
        continue

    # 开始拼接
    property_string = ''
    for i in range(len(my_property_name_list)):
        each_property = my_property_name_list[i]

        auto_property = "///\n@property (nonatomic, copy) NSString *%s;\n" % (each_property)
        property_string += auto_property
        property_string += "\n"

    whole_string = whole_string.replace("@end", property_string)
    whole_string += "\n@end"

    with open(path, 'w', encoding='utf-8', errors='ignore') as f:
        f.write(whole_string)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # 路径参数
    parser.add_argument("-path", "--path", help=".h文件的全路径")

    # 选项参数
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-swagger", "--swagger", help="如果数据来源于swagger,使用该选项", action="store_true")
    group.add_argument("-jsonDict", "--jsonDict", help="如果数据来源于Xcode打印的json数据或则json装换的字典数据,使用该选项", action="store_true")
    group.add_argument("-wiki", "--wiki", help="如果数据来源于wiki,使用该选项", action="store_true")

    # 解析参数
    args = parser.parse_args()

    # 取值
    swagger = args.swagger
    jsonDict = args.jsonDict
    wiki = args.wiki
    h_path = args.path

    # 选项不能为空
    if swagger is False and jsonDict is False and wiki is False:
        print("必须选择数据来源选项, -swagger 或者 -jsonDict 或者 -wiki")
        exit(-1)

    # 文件不能为空
    if h_path:
        code_create(h_path, swagger, wiki)

        print("----Done----")
    else:
        print(".h路径为空, 必须使用 -path 后面带上.h文件全路径")



