# Android
GS420 AI uses Capacitor to wrap the PWA into Android. The app id is `ai.gs420.app` and the web assets come from `frontend/dist`.

Workflow:
1. Build the frontend with `cd frontend && npm install && npm run build`.
2. Enter `mobile/capacitor` and run `npm install`.
3. Run `npx cap add android` once.
4. Run `npm run sync` after frontend changes.
5. Open with `npx cap open android` and build the APK in Android Studio.

The Android client does not pretend to run large models locally. Mic/file features can be exposed through Capacitor plugins later; backend connectivity is used for heavy inference.
