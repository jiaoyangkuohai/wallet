# 创建自己的钱包管理系统
## 开发备忘
1. 数据库的修改，都会引起图的自动刷新
2. 默认加载空模板
3. 修改table中的值，会引起数据库的update，并且引起自动刷新
4. 价格需要输入检查，可以输入负数，但是禁止输入“+”号
5. MySQL暂不支持，规划是支持远程数据库，要看有没有必要

## 打包编译
使用snap

## 整体图
![整体图](./img/整体图.png)