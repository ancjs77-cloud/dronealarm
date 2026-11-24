.class public Lkr/airbase/dronealarm/LocListener;
.super Ljava/lang/Object;
.source "LocListener.java"

# interfaces
.implements Landroid/location/LocationListener;

.field public static inst:Lkr/airbase/dronealarm/LocListener;
.field public static lat:D
.field public static lon:D
.field public static acc:F
.field public static t:J

.method public constructor <init>()V
    .registers 1
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V
    return-void
.end method

.method public onLocationChanged(Landroid/location/Location;)V
    .registers 4
    if-eqz p1, :end
    invoke-virtual {p1}, Landroid/location/Location;->getLatitude()D
    move-result-wide v0
    sput-wide v0, Lkr/airbase/dronealarm/LocListener;->lat:D
    invoke-virtual {p1}, Landroid/location/Location;->getLongitude()D
    move-result-wide v0
    sput-wide v0, Lkr/airbase/dronealarm/LocListener;->lon:D
    invoke-virtual {p1}, Landroid/location/Location;->getAccuracy()F
    move-result v0
    sput v0, Lkr/airbase/dronealarm/LocListener;->acc:F
    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J
    move-result-wide v0
    sput-wide v0, Lkr/airbase/dronealarm/LocListener;->t:J
    :end
    return-void
.end method

.method public onStatusChanged(Ljava/lang/String;ILandroid/os/Bundle;)V
    .registers 4
    return-void
.end method

.method public onProviderEnabled(Ljava/lang/String;)V
    .registers 2
    return-void
.end method

.method public onProviderDisabled(Ljava/lang/String;)V
    .registers 2
    return-void
.end method
