"""Applies AHMAD AIR STRIKE settings to the generated Capacitor Android project:
landscape orientation, immersive fullscreen, display cutout support, version 1.0.0."""
import re, pathlib
root = pathlib.Path('android/app')
man = root/'src/main/AndroidManifest.xml'
t = man.read_text()
if 'screenOrientation' not in t:
    t = t.replace('<activity', '<activity\n            android:screenOrientation="sensorLandscape"', 1)
man.write_text(t)

java = root/'src/main/java/com/ahmad/airstrike/MainActivity.java'
java.write_text('''package com.ahmad.airstrike;

import android.os.Build;
import android.os.Bundle;
import android.view.View;
import android.view.WindowManager;
import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        if (Build.VERSION.SDK_INT >= 28) {
            WindowManager.LayoutParams p = getWindow().getAttributes();
            p.layoutInDisplayCutoutMode = WindowManager.LayoutParams.LAYOUT_IN_DISPLAY_CUTOUT_MODE_SHORT_EDGES;
            getWindow().setAttributes(p);
        }
        immersive();
    }

    @Override
    public void onWindowFocusChanged(boolean hasFocus) {
        super.onWindowFocusChanged(hasFocus);
        if (hasFocus) immersive();
    }

    private void immersive() {
        getWindow().getDecorView().setSystemUiVisibility(
            View.SYSTEM_UI_FLAG_LAYOUT_STABLE
            | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
            | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
            | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
            | View.SYSTEM_UI_FLAG_FULLSCREEN
            | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY);
    }
}
''')

for name in ('build.gradle', 'build.gradle.kts'):
    f = root/name
    if f.exists():
        g = f.read_text()
        g = re.sub(r'versionName\s*=?\s*"[^"]*"', 'versionName "1.0.0"', g)
        f.write_text(g)
print('Android project patched')
