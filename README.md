## 通过|swagger | wiki | json | 字典 | 自动生成Objective-C模型属性
无论后端的接口文档使用的是swagger还是wiki亦或是公司直接写的一套,将文档上面的信息逐一搬到我们自己写`model`类的属性中是一件很码农的活.这里以swagger为例,介绍一个使用python脚本实现半自动转换的方式,能够生成同名属性且带上注释.同事们一起使用,再也不用担心一个奇怪的属性没有注释了.

如下图是swagger文档上面的

![swagger文档.png](https://upload-images.jianshu.io/upload_images/4103407-cb304936e69aa0fd.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


我们的目的是自动生成所有对应属性,且带上注释

```
@interface GQMatchModel : NSObject

/// 比赛状态
@property (nonatomic, copy) NSString *matchState;

/// 球探id ,
@property (nonatomic, copy) NSString *qtId;

/// 客队图片 ,
@property (nonatomic, copy) NSString *awayTeamLogo;

/// 客队id ,
@property (nonatomic, copy) NSString *awayTeamId;

/// 主队图片 ,
@property (nonatomic, copy) NSString *homeTeamLogo;

/// 主队id ,
@property (nonatomic, copy) NSString *homeTeamId;

/// 比分 ,
@property (nonatomic, copy) NSString *score;

/// 客队名 ,
@property (nonatomic, copy) NSString *awayTeamName;

/// 主队名 ,
@property (nonatomic, copy) NSString *homeTeamName;

/// 比赛时间
@property (nonatomic, copy) NSString *matchTime;

@end
```

***操作流程

**1.首先我们还是要将上面的数据一次性copy到我们新建的 `GQMatchModel `类的.h中,**

```
#import <Foundation/Foundation.h>
/*
 matchState (string, optional): 比赛状态
 qtId (string, optional): 球探id ,
 awayTeamLogo (string, optional): 客队图片 ,
 awayTeamId (string, optional): 客队id ,
 homeTeamLogo (string, optional): 主队图片 ,
 homeTeamId (string, optional): 主队id ,
 score (string, optional): 比分 ,
 awayTeamName (integer, optional): 客队名 ,
 homeTeamName (number, optional): 主队名 ,
 matchTime (number, optional): 比赛时间
 */
@interface Person : NSObject


@end

```

**2.在脚本中,读取 `GQMatchModel.h`这个文件中的字符内容,通过正则表达式或者其它方式匹配出所有属性和对应的解释**


**3.重新拼接字符串,并写入 `GQMatchModel.h`中,完成对该文件的覆写.**


这里我使用python语言进行读写操作, 并且拓展了针对wiki文档 | json字符 | 字典 自动生成属性的方式.  

使用其它语言编写转换代码也是很容易的,你可以使用其它语言重写一下逻辑,下面是针对swagger文档的转换方式.


```
def code_create_swagger(path):
    # 获取文件数据
    data = open(path, "r", encoding="utf-8", errors="ignore")

    # 读取第一行
    each = data.readline()

    # 属性列表
    my_property_name_list = list()
    # 注释列表
    my_property_annotation_list = list()
    # 存储文件原内容
    whole_string = ''

	# 遍历每一行字符,取出属性和注释内容
    while each:
        whole_string += each

        if each.find("@interface") != -1:
            each = data.readline()
            continue
		# (matchState (string, optional): 比赛状态),分析单行字符结构特点
		# 这里我们可以以 : 将属性一侧和注释一侧分割开
		# 属性一侧再使用正则匹配出第一个单词,去掉空白符,就是我们想要的
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

	# 写入原文件
    with open(path, 'w', encoding='utf-8', errors='ignore') as f:
        f.write(whole_string)
        
```

### 使用脚本

```
cd /Users/wen/PycharmProjects/MyScript
python3 auto_property.py -swagger -path /Users/wen/Documents/GitHub/funnyTry/funnyTry/funnyTry/Class/JustForFun/Playground/GQMatchModel.h
```

你可以在[这里](https://github.com/petyou/auto_property)下载该脚本玩玩.
