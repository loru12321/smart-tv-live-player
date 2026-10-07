from pathlib import Path
import re
import sys

root = Path(sys.argv[1])
# Replace the bundled photograph with a code-defined solid drawable, preserving its resource name.
photo = root / 'res/drawable-xxhdpi/vod_thumb.webp'
if photo.exists():
    photo.unlink()
(root / 'res/drawable/vod_thumb.xml').write_text('''<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="rectangle">
    <solid android:color="#101820" />
</shape>
''', encoding='utf-8')

# All BaseActivity backgrounds use a solid drawable instead of the wallpaper cache/loader.
p = root / 'smali_classes3/com/github/tvbox/osc/base/BaseActivity.smali'
s = p.read_text(encoding='utf-8')
replacement = '''.method public final OooO0OO(Z)V
    .locals 3
    invoke-virtual {p0}, Landroid/app/Activity;->getWindow()Landroid/view/Window;
    move-result-object v0
    instance-of v2, p0, Lcom/github/tvbox/osc/ui/activity/LivePlayActivity;
    if-eqz v2, :solid_background
    const/4 v1, 0x0
    invoke-virtual {v0, v1}, Landroid/view/Window;->setBackgroundDrawable(Landroid/graphics/drawable/Drawable;)V
    return-void
    :solid_background
    new-instance v1, Landroid/graphics/drawable/ColorDrawable;
    const v2, -0xefe7e0
    invoke-direct {v1, v2}, Landroid/graphics/drawable/ColorDrawable;-><init>(I)V
    invoke-virtual {v0, v1}, Landroid/view/Window;->setBackgroundDrawable(Landroid/graphics/drawable/Drawable;)V
    return-void
.end method'''
s, count = re.subn(r'\.method public final OooO0OO\(Z\)V.*?\.end method', lambda _: replacement, s, flags=re.S)
assert count == 1
p.write_text(s, encoding='utf-8')

# Changing a remote config cannot re-enable a wallpaper download from the settings button.
p = root / 'smali_classes2/com/androidx/kl0$o0OO00O.smali'
s = p.read_text(encoding='utf-8')
s, count = re.subn(r'\.method public onClick\(Landroid/view/View;\)V.*?\.end method', lambda _: '''.method public onClick(Landroid/view/View;)V
    .locals 1
    const-string v0, "直播版已使用纯色背景"
    invoke-static {v0}, Lcom/androidx/nh1;->OooO0O0(Ljava/lang/CharSequence;)V
    return-void
.end method''', s, flags=re.S)
assert count == 1
p.write_text(s, encoding='utf-8')
print('Removed bundled photo and disabled wallpaper background loading.')
