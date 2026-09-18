# GS420 AI Android
Capacitor is the canonical Android wrapper. Heavy AI inference remains on the backend/cloud/Colab; the Android app is a client.

## Build
From this directory:
npm install
npm run sync
npx cap add android
npx cap open android

For a debug APK:
npm run build

The generated Android project is intentionally created by Capacitor CLI rather than committed as a huge generated tree. Android Studio/Gradle is required to compile the APK.
