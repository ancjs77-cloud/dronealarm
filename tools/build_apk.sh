#!/bin/sh
# web/index.html → android_apk/assets 동기화 후 APK 빌드·디버그 서명 → dist/DroneAlarm.apk
# 필요: Java 17+, curl (Android SDK 불필요)
set -e
cd "$(dirname "$0")/.."
mkdir -p tools/bin tools/out
[ -f tools/bin/apktool.jar ] || curl -L -o tools/bin/apktool.jar https://github.com/iBotPeaches/Apktool/releases/download/v2.10.0/apktool_2.10.0.jar
[ -f tools/bin/uber-apk-signer.jar ] || curl -L -o tools/bin/uber-apk-signer.jar https://github.com/patrickfav/uber-apk-signer/releases/download/v1.3.0/uber-apk-signer-1.3.0.jar
cp web/index.html android_apk/assets/index.html
rm -rf tools/out/apk && mkdir -p tools/out/apk
java -jar tools/bin/apktool.jar b android_apk -o tools/out/apk/unsigned.apk
java -jar tools/bin/uber-apk-signer.jar -a tools/out/apk/unsigned.apk -o tools/out/apk/signed --allowResign
cp tools/out/apk/signed/*-aligned-debugSigned.apk dist/DroneAlarm.apk
echo "완성: dist/DroneAlarm.apk"
