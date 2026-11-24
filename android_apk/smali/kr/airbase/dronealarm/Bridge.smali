.class public Lkr/airbase/dronealarm/Bridge;
.super Ljava/lang/Object;
.source "Bridge.java"

# 자바스크립트에서 window.AndroidBridge.vibrate(ms), speak(text), stopSpeak() 로 호출

.field private ctx:Landroid/content/Context;
.field private tts:Landroid/speech/tts/TextToSpeech;

.method public constructor <init>(Landroid/content/Context;)V
    .registers 4
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V
    iput-object p1, p0, Lkr/airbase/dronealarm/Bridge;->ctx:Landroid/content/Context;
    :try_start
    new-instance v0, Landroid/speech/tts/TextToSpeech;
    const/4 v1, 0x0
    invoke-direct {v0, p1, v1}, Landroid/speech/tts/TextToSpeech;-><init>(Landroid/content/Context;Landroid/speech/tts/TextToSpeech$OnInitListener;)V
    iput-object v0, p0, Lkr/airbase/dronealarm/Bridge;->tts:Landroid/speech/tts/TextToSpeech;
    :try_end
    .catchall {:try_start .. :try_end} :catch
    :catch
    return-void
.end method

.method public vibrate(I)V
    .registers 6
    .annotation runtime Landroid/webkit/JavascriptInterface;
    .end annotation
    :try_start
    iget-object v0, p0, Lkr/airbase/dronealarm/Bridge;->ctx:Landroid/content/Context;
    const-string v1, "vibrator"
    invoke-virtual {v0, v1}, Landroid/content/Context;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;
    move-result-object v0
    check-cast v0, Landroid/os/Vibrator;
    if-eqz v0, :done
    int-to-long v1, p1
    const/4 v3, -0x1
    invoke-static {v1, v2, v3}, Landroid/os/VibrationEffect;->createOneShot(JI)Landroid/os/VibrationEffect;
    move-result-object v1
    invoke-virtual {v0, v1}, Landroid/os/Vibrator;->vibrate(Landroid/os/VibrationEffect;)V
    :try_end
    .catchall {:try_start .. :try_end} :done
    :done
    return-void
.end method

.method public speak(Ljava/lang/String;)V
    .registers 7
    .annotation runtime Landroid/webkit/JavascriptInterface;
    .end annotation
    :try_start
    iget-object v0, p0, Lkr/airbase/dronealarm/Bridge;->tts:Landroid/speech/tts/TextToSpeech;
    if-eqz v0, :done
    sget-object v1, Ljava/util/Locale;->KOREAN:Ljava/util/Locale;
    invoke-virtual {v0, v1}, Landroid/speech/tts/TextToSpeech;->setLanguage(Ljava/util/Locale;)I
    const/4 v1, 0x0
    const/4 v2, 0x0
    const-string v3, "drone"
    invoke-virtual {v0, p1, v1, v2, v3}, Landroid/speech/tts/TextToSpeech;->speak(Ljava/lang/CharSequence;ILandroid/os/Bundle;Ljava/lang/String;)I
    :try_end
    .catchall {:try_start .. :try_end} :done
    :done
    return-void
.end method

.method public stopSpeak()V
    .registers 2
    .annotation runtime Landroid/webkit/JavascriptInterface;
    .end annotation
    :try_start
    iget-object v0, p0, Lkr/airbase/dronealarm/Bridge;->tts:Landroid/speech/tts/TextToSpeech;
    if-eqz v0, :done
    invoke-virtual {v0}, Landroid/speech/tts/TextToSpeech;->stop()I
    :try_end
    .catchall {:try_start .. :try_end} :done
    :done
    return-void
.end method

.method public isApp()Z
    .registers 2
    .annotation runtime Landroid/webkit/JavascriptInterface;
    .end annotation
    const/4 v0, 0x1
    return v0
.end method

.method public getLocation()Ljava/lang/String;
    .registers 6
    .annotation runtime Landroid/webkit/JavascriptInterface;
    .end annotation
    sget-wide v0, Lkr/airbase/dronealarm/LocListener;->t:J
    const-wide/16 v2, 0x0
    cmp-long v4, v0, v2
    if-nez v4, :has
    const-string v0, ""
    return-object v0
    :has
    new-instance v0, Ljava/lang/StringBuilder;
    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V
    sget-wide v1, Lkr/airbase/dronealarm/LocListener;->lat:D
    invoke-virtual {v0, v1, v2}, Ljava/lang/StringBuilder;->append(D)Ljava/lang/StringBuilder;
    const-string v1, ","
    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    sget-wide v1, Lkr/airbase/dronealarm/LocListener;->lon:D
    invoke-virtual {v0, v1, v2}, Ljava/lang/StringBuilder;->append(D)Ljava/lang/StringBuilder;
    const-string v1, ","
    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    sget v1, Lkr/airbase/dronealarm/LocListener;->acc:F
    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(F)Ljava/lang/StringBuilder;
    const-string v1, ","
    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    sget-wide v1, Lkr/airbase/dronealarm/LocListener;->t:J
    invoke-virtual {v0, v1, v2}, Ljava/lang/StringBuilder;->append(J)Ljava/lang/StringBuilder;
    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;
    move-result-object v0
    return-object v0
.end method
