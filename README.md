# Location-Laborer 不完整地址补全建议与地理编码

在进行大气污染或气象因素与健康的关联研究时，可能会存在研究对象填写地址时准确填写了街道、小区名却忽略了省市区信息的情况。由于主流地理编码产品需提供结构化地址（由大区域名称到小区域名称组合的地址，规则遵循：国家、省份、城市、区县、城镇、乡村、街道、门牌号码、屋邨、大厦），若直接对省市区缺省的地址信息进行地理编码，则有一定可能获得错误的经纬度结果。这种情况下，研究对象实际上已提供较为准确的地址信息，若因此导致错误或被排除，则会造成样本的不必要流失。研究者对不完整地址进行补全可减少错误与损失，但进行查询补全的工作将占用较多时间，且较为繁琐重复。

Location-Laborer 是一款使用 python 编程语言开发的应用，它可以帮助用户处理缺少省、市、区信息的不完整地址。该应用基于高德地图的输入提示与地理编码产品，为用户提供可能的完整地址建议，并获取该地址对应的经纬度。该应用旨在提高研究者补全地址的效率，节省研究者的时间和精力。

- 输入提示：当用户输入地址的部分信息时，应用会给出补全建议。相比于地理编码的结构化地址，输入提示基于关键词进行查询，与地理编码相同，输入提示也可以返回建议地址的经纬度信息。
- 地理编码：当用户输入地址（包括不完整地址）时，应用会使用高德地图的地理编码接口，将地址转换为经纬度坐标，方便研究者进行后续的暴露评估。
- 目前仅支持导入包含不完整地址列的`csv`文件（UTF-8 编码）进行后续操作，暂不支持直接输入地址 ~~（如果不完整地址数量少到手动就可以打完的话那也根本不需要这个玩意儿了 orz）~~
- 导入`csv`文件后会检查`final_address`, `final_lon`, `final_lat`, `geo_info`, `suggest_info`这几列的存在，如果不存在则创建相应列，如果已存在会从顺数第一空白行开始（做不完可以先导出，再导入就会从上次没完成的地方开始）

**使用 Location-Laborer 需要先申请高德地图应用 Key。申请步骤相当简单且无需等待，请参考高德地图官方文档[成为开发者并创建 key](https://lbs.amap.com/api/webservice/guide/create-project/get-key)**

这里是一个操作示范视频：
[![Getting Started with Location-Laborer](https://img.youtube.com/vi/DUaZFWqIZ_w/sddefault.jpg)](https://youtu.be/DUaZFWqIZ_w)

---

# Location-Laborer: An application gets suggestions on incomplete address and perform geocoding.

In studies examining the association between air pollution or meteorological factors and health outcomes, it is possible for participants to accurately report the street or community but omitting information pertaining to provinces and cities. Geocoding products typically require the input of structured addresses, which follow a hierarchical format from larger to smaller regional names (i.e., province, city, district, county, town, village, street, door number, estate, building). If an address is geocoded without including information about the province and city, the resulting latitude and longitude coordinates may be incorrect. In such cases, even if the incomplete address provided by participants is relatively accurate at the street or community level, it may still result in incorrect geocoding. This could further lead to the exclusion of participants and a reduction in sample size.

Location-Laborer is an application developed using the Python programming language. It assists researchers in filling in addresses that lack information about the province, city, or district. Location-Laborer uses Amap’s input prompts and geocoding protocol to provide suggestions for complete addresses, and obtains the corresponding longitude and latitude for the address at the same time. The goal of Location-Laborer is to improve the efficiency of filling in addresses and thus save researchers' time and energy.

- Input prompt: When a user enters part of an address, the application provides suggestions for completing it. Unlike geocoding, which uses structured addresses, input prompts query based on keywords. Like geocoding, input prompts can also return the latitude and longitude information of the suggested address.
- Geocoding: When a user enters an address, including an incomplete one, the application uses Amap’s geocoding services to convert the address into latitude and longitude coordinates. This allows researchers to conduct subsequent exposure assessments.
- Location-Laborer only supports importing UTF-8 encoding `csv` files that contain one column with incomplete addresses for subsequent operations. It does not support directly typing in addresses currently.
- Upon importing a `csv` file, Location-Laborer checks for the existence of the `final_address`, `final_lon`, `final_lat`, `geo_info`, and `suggest_info` columns. If these columns do not exist, they will be created. If they already exist, the application will start with the first blank line in the sequence. In other words, if the process is not finished, you can export the file and continue from where you left off when you import it again.

**To use Location-Laborer, you must apply for an Amap application key. The application process is simple and does not require any waiting. Please refer to the Amap documentation on [Becoming a Developer and Creating a Key](https://lbs.amap.com/api/webservice/guide/create-project/get-key) for more information.**

~~说真的，这个应该提名个“最无用应用”，毕竟世界上真的会有第二个课题组需要手动检查接近 10 万条地址信息吗 orz~~
