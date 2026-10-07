# 影视仓直播专用版

以用户提供的影视仓 APK 的直播功能为基础进行本地定制，不是从零开发的独立播放器。

## 本次范围

- 独立包名 `com.ysc.live.elder`，应用名“影视仓·直播”，保留原应用数据。
- 启动直达原生直播，首次没有直播源时自动配置指定的完整 pllive.txt。
- 保留地区、运营商和多线路，不过滤任何分组。
- 全屏短按确认打开选台菜单；长按确认收藏/取消收藏当前频道，释放不再打开菜单。
- 列表内沿用原版长按收藏，方向键选台、左右切换分组和列表、返回收起。
- 深色高对比菜单，增大字体，菜单顶部显示操作说明。
- 移除内置人像壁纸，普通页面使用纯色背景，直播页面保持视频层透明；在线换壁纸入口关闭。
- 保留原播放内核、换线路和直播设置，启动不进入点播首页。

## 验证

在已连接的海信 VIDAA_TV 上进行独立安装、首次加载、播放、遥控器短按/长按、收藏持久化及重启测试。
第三方直播线路的实时可用性取决于源站和电视网络，不能通过 APK 保证所有线路可播放。

## 构建

`patch.py` 对已有解包工程的副本应用补丁，原始 APK 和解包目录均保留。
补丁代码位于本目录；原 APK 的资源和播放内核不作为自研代码发布。

依次在全新工程副本上执行：

```powershell
python live-customization/patch.py C:/Users/loru/ysc-live-build
python live-customization/fix-startup.py C:/Users/loru/ysc-live-build
python live-customization/remove-background.py C:/Users/loru/ysc-live-build
& 'C:/Program Files/Eclipse Adoptium/jdk-17.0.20.101-hotspot/bin/java.exe' -jar apktool.jar b C:/Users/loru/ysc-live-build -o C:/Users/loru/ysc-live-build/live-unsigned.apk
./live-customization/sign.ps1
```

签名密钥保存在用户目录 `.android/ysc-live-signing`，后续覆盖更新须继续使用此密钥，不要提交到 Git。

## 2026-10-07 真机验证结果

- 海信 `VIDAA_TV` / Android 11 / ARMv7：独立安装成功，原 `com.ysc.tvbox` 保留。
- 未手工导入配置，启动自动下载指定直播源，显示山东联通、四川移动、广东电信等原始分组。
- 首次启动选择 CCTV1；部分测试线路响应失败会沿用原版自动切换机制。没有承诺所有线路可用。
- 修复不透明窗口背景遮挡电视硬件视频层的问题，CCTV8 显示实际视频；日志确认 1920×1080 和 MEDIA_INFO_VIDEO_RENDERING_START。
- 全屏长按确认收藏 CCTV8，再次长按出现“已取消收藏”；不会误打开菜单。
- 再次收藏后强制停止并重新启动，续播 CCTV8；收藏列表中 CCTV8 仍然存在。
- 短按确认、左右/上下导航均已实测；菜单显示大字操作提示。
- 最终 APK 中不存在 `vod_thumb.webp`，同名资源为纯色 XML；在线换壁纸点击不再发起下载。
- APK 签名验证通过 v1、v2、v3。

安装包：`发布/影视仓直播版/影视仓直播版-2026.10.apk`。
