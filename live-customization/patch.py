from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

root = Path(sys.argv[1])
scripts = Path(__file__).parent

def edit(relative, transform):
    p = root / relative
    p.write_text(transform(p.read_text(encoding='utf-8')), encoding='utf-8')

edit('AndroidManifest.xml', lambda s: s.replace('gsq.gdwkqb.pgytbgutv.jkv605', 'com.ysc.live.elder')
     .replace('android:label="影视仓"', 'android:label="影视仓·直播"')
     .replace('android:debuggable="true"', 'android:debuggable="false"'))
edit('apktool.yml', lambda s: s.replace('renameManifestPackage: com.ysc.tvbox', 'renameManifestPackage: com.ysc.live.elder')
     .replace('versionCode: 152', 'versionCode: 153').replace('versionName: 2026', "versionName: '2026.10-live1'"))

activity = 'smali_classes2/com/github/tvbox/osc/ui/activity/LivePlayActivity.smali'
source_default = '''
    if-eqz v6, :live_default_create
    invoke-virtual {v6}, Lcom/github/tvbox/osc/bean/LiveSourceBean;->getSourceUrl()Ljava/lang/String;
    move-result-object v7
    invoke-static {v7}, Landroid/text/TextUtils;->isEmpty(Ljava/lang/CharSequence;)Z
    move-result v7
    if-eqz v7, :live_default_ready
    :live_default_create
    new-instance v6, Lcom/github/tvbox/osc/bean/LiveSourceBean;
    invoke-direct {v6}, Lcom/github/tvbox/osc/bean/LiveSourceBean;-><init>()V
    const-string v7, "https://gh-proxy.org/https://raw.githubusercontent.com/jn950/live/main/tv/pllive.txt"
    invoke-virtual {v6, v7}, Lcom/github/tvbox/osc/bean/LiveSourceBean;->setSourceUrl(Ljava/lang/String;)V
    const-string v7, "全国直播 · 完整地区线路"
    invoke-virtual {v6, v7}, Lcom/github/tvbox/osc/bean/LiveSourceBean;->setName(Ljava/lang/String;)V
    invoke-virtual {v6, v7}, Lcom/github/tvbox/osc/bean/LiveSourceBean;->setSourceName(Ljava/lang/String;)V
    const-string v7, "live_source_url_current"
    invoke-static {v7, v6}, Lcom/orhanobut/hawk/Hawk;->put(Ljava/lang/String;Ljava/lang/Object;)Z
    :live_default_ready
'''

def patch_activity(s):
    assert 'liveConfirmActive' not in s, 'Use a fresh copy of the input project'
    marker = '# instance fields'
    s = s.replace(marker, marker + '\n.field private liveConfirmActive:Z\n.field private liveConfirmHeld:Z\n', 1)
    marker = '    invoke-virtual {v1, v6}, Lcom/androidx/o0oO0Ooo;->selectLiveUrlAndLoad(Lcom/github/tvbox/osc/bean/LiveSourceBean;)V'
    assert s.count(marker) == 1
    s = s.replace(marker, source_default + '\n' + marker)
    marker = '.method public onPause()V\n    .locals 1'
    s = s.replace(marker, marker + '''
    const/4 v0, 0x0
    iput-boolean v0, p0, Lcom/github/tvbox/osc/ui/activity/LivePlayActivity;->liveConfirmActive:Z
    iput-boolean v0, p0, Lcom/github/tvbox/osc/ui/activity/LivePlayActivity;->liveConfirmHeld:Z
''')
    return s + '\n' + (scripts / 'live-methods.smali').read_text(encoding='utf-8')

edit(activity, patch_activity)

android = 'http://schemas.android.com/apk/res/android'
app = 'http://schemas.android.com/apk/res-auto'
ET.register_namespace('android', android)
ET.register_namespace('app', app)
A = lambda k: '{' + android + '}' + k
p = root / 'res/layout/activity_live_play.xml'
tree = ET.parse(p)
panel = next(n for n in tree.iter() if n.get(A('id')) == '@id/tvLeftChannnelListLayout')
children = list(panel)
for child in children:
    panel.remove(child)
panel.set(A('orientation'), 'vertical')
panel.set(A('paddingTop'), '16dp')
panel.set(A('paddingBottom'), '16dp')
header = ET.SubElement(panel, 'TextView', {
    A('layout_width'): 'match_parent', A('layout_height'): 'wrap_content',
    A('paddingLeft'): '18dp', A('paddingRight'): '18dp', A('paddingBottom'): '10dp',
    A('textSize'): '18sp', A('textColor'): '#FFFFFFFF',
    A('text'): '选台菜单   ·   长按确定收藏\n左右选分类　上下选节目　确定观看',
    A('focusable'): 'false', A('maxLines'): '2'
})
body = ET.SubElement(panel, 'LinearLayout', {A('orientation'): 'horizontal',
    A('layout_width'): 'wrap_content', A('layout_height'): '0dp', A('layout_weight'): '1'})
for child in children:
    body.append(child)
tree.write(p, encoding='utf-8', xml_declaration=True)
edit('res/drawable/bg_channel_list.xml', lambda s: s.replace('#cc181e28', '#f2181e28'))
edit('res/layout/item_live_channel.xml', lambda s: s.replace('android:textSize="22.0mm"', 'android:textSize="22sp"').replace('android:gravity="left"', 'android:gravity="center_vertical|left"'))
edit('res/layout/item_live_channel_group.xml', lambda s: s.replace('android:textSize="@dimen/ts_22"', 'android:textSize="22sp"'))
print('Patched live startup, complete default source, remote favorites, and readable menu.')
