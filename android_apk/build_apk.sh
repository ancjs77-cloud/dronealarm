#!/bin/sh
# 드론경보 APK 다시 만들기 (Java 17 필요)
# 1) apktool_2.10.0.jar, uber-apk-signer-1.3.0.jar 를 이 폴더에 둡니다 (GitHub 릴리스에서 내려받기)
# 2) assets/index.html 을 고친 뒤 실행: sh build_apk.sh
set -e
java -jar apktool_2.10.0.jar b . -o droneAlarm-unsigned.apk
java -jar uber-apk-signer-1.3.0.jar -a droneAlarm-unsigned.apk -o out --allowResign
echo "완성: out/ 폴더의 *-aligned-debugSigned.apk"
