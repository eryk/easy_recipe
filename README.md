# easy_recipe
今天吃什么？

做饭久了这问题越来越难想了。。。这项目是抓取美食杰、美食天下和下厨房的菜谱，一共3500多个菜，每次访问web页面随机出7个菜

在web.py文件里设置ban_words去掉了我不爱吃的菜

```python
ban_words = ['爪', '舌']
```
