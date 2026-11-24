.class public Lkr/airbase/dronealarm/MainActivity;
.super Landroid/app/Activity;
.source "MainActivity.java"

# 웹 화면(assets/index.html)을 띄우는 단일 액티비티.
# 화면 꺼짐 방지, 잠금화면 위 표시, 자바스크립트용 진동·음성 브리지 제공.

.field private web:Landroid/webkit/WebView;

.method public constructor <init>()V
    .registers 1
    invoke-direct {p0}, Landroid/app/Activity;-><init>()V
    return-void
.end method

.method protected onCreate(Landroid/os/Bundle;)V
    .registers 6

    invoke-super {p0, p1}, Landroid/app/Activity;->onCreate(Landroid/os/Bundle;)V

    # FLAG_KEEP_SCREEN_ON(0x80) | FLAG_SHOW_WHEN_LOCKED(0x80000) | FLAG_TURN_SCREEN_ON(0x200000)
    invoke-virtual {p0}, Lkr/airbase/dronealarm/MainActivity;->getWindow()Landroid/view/Window;
    move-result-object v0
    const v1, 0x280080
    invoke-virtual {v0, v1}, Landroid/view/Window;->addFlags(I)V

    new-instance v0, Landroid/webkit/WebView;
    invoke-direct {v0, p0}, Landroid/webkit/WebView;-><init>(Landroid/content/Context;)V
    iput-object v0, p0, Lkr/airbase/dronealarm/MainActivity;->web:Landroid/webkit/WebView;

    invoke-virtual {v0}, Landroid/webkit/WebView;->getSettings()Landroid/webkit/WebSettings;
    move-result-object v1
    const/4 v2, 0x1
    const/4 v3, 0x0
    invoke-virtual {v1, v2}, Landroid/webkit/WebSettings;->setJavaScriptEnabled(Z)V
    invoke-virtual {v1, v2}, Landroid/webkit/WebSettings;->setDomStorageEnabled(Z)V
    invoke-virtual {v1, v3}, Landroid/webkit/WebSettings;->setMediaPlaybackRequiresUserGesture(Z)V

    new-instance v1, Landroid/webkit/WebChromeClient;
    invoke-direct {v1}, Landroid/webkit/WebChromeClient;-><init>()V
    invoke-virtual {v0, v1}, Landroid/webkit/WebView;->setWebChromeClient(Landroid/webkit/WebChromeClient;)V

    new-instance v1, Lkr/airbase/dronealarm/Bridge;
    invoke-direct {v1, p0}, Lkr/airbase/dronealarm/Bridge;-><init>(Landroid/content/Context;)V
    const-string v2, "AndroidBridge"
    invoke-virtual {v0, v1, v2}, Landroid/webkit/WebView;->addJavascriptInterface(Ljava/lang/Object;Ljava/lang/String;)V

    const-string v1, "file:///android_asset/index.html"
    invoke-virtual {v0, v1}, Landroid/webkit/WebView;->loadUrl(Ljava/lang/String;)V

    invoke-virtual {p0, v0}, Lkr/airbase/dronealarm/MainActivity;->setContentView(Landroid/view/View;)V

    invoke-direct {p0}, Lkr/airbase/dronealarm/MainActivity;->askLocation()V
    return-void
.end method

# 위치 권한이 없으면 요청, 있으면 바로 위치 갱신 시작
.method private askLocation()V
    .registers 5
    :try_start
    const-string v0, "android.permission.ACCESS_FINE_LOCATION"
    invoke-virtual {p0, v0}, Lkr/airbase/dronealarm/MainActivity;->checkSelfPermission(Ljava/lang/String;)I
    move-result v1
    if-nez v1, :need
    invoke-direct {p0}, Lkr/airbase/dronealarm/MainActivity;->startLoc()V
    goto :done
    :need
    const/4 v1, 0x2
    new-array v1, v1, [Ljava/lang/String;
    const/4 v2, 0x0
    aput-object v0, v1, v2
    const-string v0, "android.permission.ACCESS_COARSE_LOCATION"
    const/4 v2, 0x1
    aput-object v0, v1, v2
    const/16 v2, 0x65
    invoke-virtual {p0, v1, v2}, Lkr/airbase/dronealarm/MainActivity;->requestPermissions([Ljava/lang/String;I)V
    :try_end
    .catchall {:try_start .. :try_end} :done
    :done
    return-void
.end method

.method public onRequestPermissionsResult(I[Ljava/lang/String;[I)V
    .registers 4
    invoke-direct {p0}, Lkr/airbase/dronealarm/MainActivity;->startLoc()V
    return-void
.end method

# GPS·네트워크 위치를 1초 간격으로 받아 LocListener 정적 필드에 저장
.method private startLoc()V
    .registers 8
    :try_start
    const-string v0, "android.permission.ACCESS_COARSE_LOCATION"
    invoke-virtual {p0, v0}, Lkr/airbase/dronealarm/MainActivity;->checkSelfPermission(Ljava/lang/String;)I
    move-result v0
    if-nez v0, :done
    const-string v0, "location"
    invoke-virtual {p0, v0}, Lkr/airbase/dronealarm/MainActivity;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;
    move-result-object v0
    check-cast v0, Landroid/location/LocationManager;
    if-eqz v0, :done
    new-instance v5, Lkr/airbase/dronealarm/LocListener;
    invoke-direct {v5}, Lkr/airbase/dronealarm/LocListener;-><init>()V
    sput-object v5, Lkr/airbase/dronealarm/LocListener;->inst:Lkr/airbase/dronealarm/LocListener;

    const-string v1, "gps"
    invoke-virtual {v0, v1}, Landroid/location/LocationManager;->getLastKnownLocation(Ljava/lang/String;)Landroid/location/Location;
    move-result-object v6
    invoke-virtual {v5, v6}, Lkr/airbase/dronealarm/LocListener;->onLocationChanged(Landroid/location/Location;)V

    const-wide/16 v2, 0x3e8
    const/4 v4, 0x0
    invoke-virtual/range {v0 .. v5}, Landroid/location/LocationManager;->requestLocationUpdates(Ljava/lang/String;JFLandroid/location/LocationListener;)V
    :try_end
    .catchall {:try_start .. :try_end} :done
    :try_start2
    const-string v1, "network"
    const-wide/16 v2, 0x3e8
    const/4 v4, 0x0
    invoke-virtual/range {v0 .. v5}, Landroid/location/LocationManager;->requestLocationUpdates(Ljava/lang/String;JFLandroid/location/LocationListener;)V
    :try_end2
    .catchall {:try_start2 .. :try_end2} :done
    :done
    return-void
.end method

.method public onBackPressed()V
    .registers 4
    iget-object v0, p0, Lkr/airbase/dronealarm/MainActivity;->web:Landroid/webkit/WebView;
    if-eqz v0, :cond_super
    const-string v1, "window.onAndroidBack && window.onAndroidBack()"
    const/4 v2, 0x0
    invoke-virtual {v0, v1, v2}, Landroid/webkit/WebView;->evaluateJavascript(Ljava/lang/String;Landroid/webkit/ValueCallback;)V
    return-void
    :cond_super
    invoke-super {p0}, Landroid/app/Activity;->onBackPressed()V
    return-void
.end method
