用Django实现一个文档共享平台



规划

1. 上传：浏览器/命令行(requests.post)/客户端/大文件/大小限制/断点续传/秒传
2. 存储：sha1/目录结构/相对路径
3. 展示：列表/详情/树形/搜索/分页 (ListView, DetailView, 瀑布流)
4. 下载：匿名下载/登录下载/提取码下载
5. 用户：注册/登入/登出/验证码
6. 共享：提取码/有效期
7. 客户端：大文件/断点续传/批量上传下载/上传下载目录
8. 文件管理：元信息编辑/删除文件 (文件名，上传者，上传日期，……）
9. API：内部API/外部RESTful (http/https)




参考资料：

1. 搜索引擎 (baidu, bing, google)
2. Django官方文档 https://docs.djangoproject.com/en/1.11/
3. Django官方文档中译版 http://usyiyi.cn
4. git参考 http://www.bootcss.com/p/git-guide/
