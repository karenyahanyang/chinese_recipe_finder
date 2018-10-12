package com.example.android.dishclassifier;

/**
 * Created by admin on 2018-02-25.
 */
import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.content.Intent;

public class MyActivity extends Activity {
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.my_activity);
    }

    public void open_camera(View view)
    {
        Intent intent = new Intent(view.getContext(), CameraActivity.class);
        startActivityForResult(intent, 0);
    }

    public void open_voice(View view)
    {
        Intent intent = new Intent(view.getContext(), HoundifyVoiceSearchWithPhraseSpotterActivity.class);
        startActivityForResult(intent, 0);
    }

    public void open_recipes(View view)
    {
        Intent intent = new Intent(view.getContext(), RecipeMenuActivity.class);
        startActivityForResult(intent, 0);
    }
}
