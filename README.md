# comfyui-setu
通过api拉取图片来实现图片反推
本项目使用了由 [lolisuki Api](https://lolisuki.cn/) 提供的API支持，特此感谢。
通过该API，我们能够实现以下功能：
从此api拉取你想要的图片,进行图片反推来ai重绘

插件安装方式:
~\custom_nodes\comfyui_setu文件夹输入:\n
[git clone https://github.com/vzicecc/comfyui-setu.git]

此插件获取到图片后输出的是图片路径,因此需要以路径加载图片,如下图所示:
![QQ_1735125746649](https://github.com/user-attachments/assets/1d18097d-7f5b-4917-8836-ff051c41f850)
历史获取到的图片储存在~\image-save\save文件夹下

插件选项说明:
r18后面数字:是否包含 R-18 ，0为不包含，1为只包含 R18，2为包括 R18 和 非R18

num=返回图片数量\n
ai=是否包含ai图片 0=不包含 1=包含 \n
gif=是否包含gif图片 0=不包含 1=包含 \n
proxy=代理 \n
level=涩涩度 范围1-6(6可能含r18g) \n
taste=图片类型，可以同时指定多个类型，多个类型之间用逗号隔开 \n
      0：随机 \n
      1：萝莉 \n
      2：少女 \n
      3：御姐 \n

tag=Tag 参数可以通过&符号连接多个。Tag 之间用|符号隔开时，代表只需要匹配其中任意一个, \n
例如想要查找（萝莉或者少女) 并且带有 (白丝或者黑丝) 的色图可以这样发送请求  \n
萝莉|少女&tag=白丝|黑丝
