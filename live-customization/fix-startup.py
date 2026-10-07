from pathlib import Path
import sys
root = Path(sys.argv[1])
p = root / 'smali_classes2/com/github/tvbox/osc/ui/activity/LivePlayActivity.smali'
s = p.read_text(encoding='utf-8')
s = s.replace('    if-nez v6, :live_default_ready', '''    if-eqz v6, :live_default_create
    invoke-virtual {v6}, Lcom/github/tvbox/osc/bean/LiveSourceBean;->getSourceUrl()Ljava/lang/String;
    move-result-object v7
    invoke-static {v7}, Landroid/text/TextUtils;->isEmpty(Ljava/lang/CharSequence;)Z
    move-result v7
    if-eqz v7, :live_default_ready
    :live_default_create''')
start = s.index('.method public final OooOo()V')
end = s.index('.end method', start)
m = s[start:end]
m = m.replace('.locals 9', '.locals 10')
m = m.replace(':cond_0\n    const-string v1, ""', ':cond_0\n    const-string v1, "CCTV1"')
m = m.replace('    invoke-virtual {v8}, Lcom/github/tvbox/osc/bean/LiveChannelItem;->getChannelName()',
              '    move-object v9, v8\n\n    invoke-virtual {v8}, Lcom/github/tvbox/osc/bean/LiveChannelItem;->getChannelName()')
m = m.replace('invoke-virtual {v0}, Lcom/github/tvbox/osc/bean/LiveChannelItem;->getChannelIndex()',
              'invoke-virtual {v9}, Lcom/github/tvbox/osc/bean/LiveChannelItem;->getChannelIndex()')
s = s[:start] + m + s[end:]
p.write_text(s, encoding='utf-8')
