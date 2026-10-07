.method public toggleWatchingFavorite()V
    .locals 5
    iget-object v0, p0, Lcom/github/tvbox/osc/ui/activity/LivePlayActivity;->OooOoo0:Lcom/github/tvbox/osc/bean/LiveChannelItem;
    if-eqz v0, :done
    iget-object v1, p0, Lcom/github/tvbox/osc/ui/activity/LivePlayActivity;->OooOoO0:Ljava/util/List;
    invoke-interface {v1}, Ljava/util/List;->isEmpty()Z
    move-result v2
    if-nez v2, :done
    const/4 v2, 0x0
    invoke-interface {v1, v2}, Ljava/util/List;->get(I)Ljava/lang/Object;
    move-result-object v1
    check-cast v1, Lcom/github/tvbox/osc/bean/LiveChannelGroup;
    invoke-virtual {v1}, Lcom/github/tvbox/osc/bean/LiveChannelGroup;->getLiveChannels()Ljava/util/ArrayList;
    move-result-object v2
    iget-boolean v3, v0, Lcom/github/tvbox/osc/bean/LiveChannelItem;->isCollected:Z
    xor-int/lit8 v3, v3, 0x1
    iput-boolean v3, v0, Lcom/github/tvbox/osc/bean/LiveChannelItem;->isCollected:Z
    if-eqz v3, :remove
    invoke-virtual {v0}, Lcom/github/tvbox/osc/bean/LiveChannelItem;->clone()Lcom/github/tvbox/osc/bean/LiveChannelItem;
    move-result-object v0
    invoke-virtual {v2}, Ljava/util/ArrayList;->size()I
    move-result v3
    invoke-virtual {v0, v3}, Lcom/github/tvbox/osc/bean/LiveChannelItem;->setChannelIndex(I)V
    invoke-virtual {v2, v0}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z
    const-string v0, "已收藏，打开选台菜单可在收藏中找到"
    goto :save
    :remove
    invoke-virtual {v2, v0}, Ljava/util/ArrayList;->remove(Ljava/lang/Object;)Z
    const/4 v3, 0x0
    :reindex
    invoke-virtual {v2}, Ljava/util/ArrayList;->size()I
    move-result v4
    if-ge v3, v4, :removed
    invoke-virtual {v2, v3}, Ljava/util/ArrayList;->get(I)Ljava/lang/Object;
    move-result-object v0
    check-cast v0, Lcom/github/tvbox/osc/bean/LiveChannelItem;
    invoke-virtual {v0, v3}, Lcom/github/tvbox/osc/bean/LiveChannelItem;->setChannelIndex(I)V
    add-int/lit8 v3, v3, 0x1
    goto :reindex
    :removed
    const-string v0, "已取消收藏"
    :save
    invoke-static {v0}, Lcom/androidx/nh1;->OooO0O0(Ljava/lang/CharSequence;)V
    const-string v0, "live_chanele_collectd"
    invoke-static {v0, v1}, Lcom/orhanobut/hawk/Hawk;->put(Ljava/lang/String;Ljava/lang/Object;)Z
    iget-object v0, p0, Lcom/github/tvbox/osc/ui/activity/LivePlayActivity;->OooOOOo:Lcom/androidx/wd0;
    if-eqz v0, :done
    invoke-virtual {v0}, Landroidx/recyclerview/widget/RecyclerView$Adapter;->notifyDataSetChanged()V
    :done
    return-void
.end method

.method public dispatchKeyEvent(Landroid/view/KeyEvent;)Z
    .locals 5
    invoke-virtual {p1}, Landroid/view/KeyEvent;->getKeyCode()I
    move-result v0
    const/16 v1, 0x17
    if-eq v0, v1, :center
    const/16 v1, 0x42
    if-ne v0, v1, :normal
    :center
    iget-object v0, p0, Lcom/github/tvbox/osc/ui/activity/LivePlayActivity;->OooOOo:Landroid/widget/LinearLayout;
    if-eqz v0, :normal
    iget-boolean v0, p0, Lcom/github/tvbox/osc/ui/activity/LivePlayActivity;->liveConfirmActive:Z
    if-nez v0, :handle
    invoke-virtual {p0}, Lcom/github/tvbox/osc/ui/activity/LivePlayActivity;->OooOoO()Z
    move-result v0
    if-nez v0, :normal
    invoke-virtual {p1}, Landroid/view/KeyEvent;->getAction()I
    move-result v0
    if-nez v0, :normal
    const/4 v0, 0x1
    iput-boolean v0, p0, Lcom/github/tvbox/osc/ui/activity/LivePlayActivity;->liveConfirmActive:Z
    const/4 v0, 0x0
    iput-boolean v0, p0, Lcom/github/tvbox/osc/ui/activity/LivePlayActivity;->liveConfirmHeld:Z
    :handle
    invoke-virtual {p1}, Landroid/view/KeyEvent;->isCanceled()Z
    move-result v0
    if-nez v0, :cancel
    iget-boolean v0, p0, Lcom/github/tvbox/osc/ui/activity/LivePlayActivity;->liveConfirmHeld:Z
    if-nez v0, :release
    invoke-virtual {p1}, Landroid/view/KeyEvent;->isLongPress()Z
    move-result v0
    if-nez v0, :favorite
    invoke-virtual {p1}, Landroid/view/KeyEvent;->getEventTime()J
    move-result-wide v0
    invoke-virtual {p1}, Landroid/view/KeyEvent;->getDownTime()J
    move-result-wide v2
    sub-long/2addr v0, v2
    const-wide/16 v2, 0x2bc
    cmp-long v4, v0, v2
    if-ltz v4, :release
    :favorite
    const/4 v0, 0x1
    iput-boolean v0, p0, Lcom/github/tvbox/osc/ui/activity/LivePlayActivity;->liveConfirmHeld:Z
    invoke-virtual {p0}, Lcom/github/tvbox/osc/ui/activity/LivePlayActivity;->toggleWatchingFavorite()V
    :release
    invoke-virtual {p1}, Landroid/view/KeyEvent;->getAction()I
    move-result v0
    const/4 v1, 0x1
    if-ne v0, v1, :consumed
    iget-boolean v0, p0, Lcom/github/tvbox/osc/ui/activity/LivePlayActivity;->liveConfirmHeld:Z
    if-nez v0, :cancel
    invoke-virtual {p0}, Lcom/github/tvbox/osc/ui/activity/LivePlayActivity;->Oooo0OO()V
    :cancel
    const/4 v0, 0x0
    iput-boolean v0, p0, Lcom/github/tvbox/osc/ui/activity/LivePlayActivity;->liveConfirmActive:Z
    iput-boolean v0, p0, Lcom/github/tvbox/osc/ui/activity/LivePlayActivity;->liveConfirmHeld:Z
    :consumed
    const/4 v0, 0x1
    return v0
    :normal
    invoke-super {p0, p1}, Lcom/github/tvbox/osc/base/BaseActivity;->dispatchKeyEvent(Landroid/view/KeyEvent;)Z
    move-result v0
    return v0
.end method
