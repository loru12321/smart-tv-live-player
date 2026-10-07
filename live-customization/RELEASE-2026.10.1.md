# 影视仓·直播 2026.10.1

基于用户提供的“影视仓(2026多配置版).apk”进行直播定制，保留原播放内核。

## 更新

- 启动直接进入直播，之后续播上次频道。
- 自动配置完整直播源，保留地区、运营商及多线路分组。
- 全屏长按确认收藏/取消收藏，短按确认打开选台菜单。
- 大字深色菜单，增加遥控器操作说明。
- 移除内置人像壁纸，关闭在线换壁纸入口。
- 独立包名 `com.ysc.live.elder`，可与原影视仓共存。

默认直播源：
https://gh-proxy.org/https://raw.githubusercontent.com/jn950/live/main/tv/pllive.txt

## 验证

已在海信 VIDAA_TV（Android 11，ARMv7）上验证安装、源自动载入、CCTV-8 视频播放、遥控器操作及收藏重启保留。APK 签名验证通过 v1/v2/v3。线路可用性受源站和网络影响，未逐一验证全部频道。

APK 内部版本：`2026.10-live1`，versionCode `153`。本次 Release 使用日期版本标签。

SHA256：`F5B11B97BD78D9858386C0D50E77057A1083C6EC1B0DB0A097E9EF2BD68D2AAE`
