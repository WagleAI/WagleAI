package com.sample.mask;

import android.app.Activity;
import android.app.AlertDialog;
import android.app.Dialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.graphics.PointF;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import com.google.android.material.snackbar.Snackbar;
import com.naver.maps.geometry.LatLng;
import com.naver.maps.map.CameraPosition;
import com.naver.maps.map.MapFragment;
import com.naver.maps.map.MapView;
import com.naver.maps.map.NaverMap;
import com.naver.maps.map.NaverMapOptions;
import com.naver.maps.map.OnMapReadyCallback;
import com.naver.maps.map.UiSettings;
import com.naver.maps.map.overlay.InfoWindow;
import com.naver.maps.map.overlay.Marker;
import com.naver.maps.map.overlay.Overlay;
import com.naver.maps.map.overlay.OverlayImage;
import com.naver.maps.map.util.FusedLocationSource;

public class MapsNaverActivity extends AppCompatActivity implements OnMapReadyCallback, Overlay.OnClickListener { //, NaverMap.OnMapClickListener, Overlay.OnClickListener, NaverMap.OnCameraChangeListener{

    private static final int ACCESSIBILITY_LOCATION_PERMISSION_REQUEST_CODE = 100;

    private FusedLocationSource locationSource;
    private MapView mapView;
    private NaverMap naverMap;
    private InfoWindow minfoWindow;
    private boolean mIsCameraAnimated = false;

    TextView  textView;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_maps_naver);

        textView = (TextView) findViewById(R.id.textView);

        mapView = findViewById(R.id.map_view);
        mapView.getMapAsync(this);
    }

    @Override
    public void onMapReady(@NonNull NaverMap naverMap) {

        double[][] latlon = {   {37.5670135, 126.9783740},
                                {37.56, 126.97},
                                {37.53, 126.98},
                                {37.55, 126.95},
                                {37.50, 126.99},
                                {37.54, 129.94},
                                {37.58, 126.93},
                                {37.49, 126.96},
                                {37.57, 127.},
                                {37.50, 126.95} };

        Marker [] markers = new Marker[latlon.length];

        //System.out.println(markers[0]);

        for(int i=0;i<markers.length;i++) {
            markers[i] = new Marker();
            markers[i].setPosition(new LatLng(latlon[i][0], latlon[i][1]));
            markers[i].setMap(naverMap);
            final int popnumb = i;
            System.out.println(popnumb);
            markers[i].setOnClickListener(new Overlay.OnClickListener() {
                @Override
                public boolean onClick(@NonNull Overlay overlay) {
                    if (popnumb > 3) {
                        showMessage1();
                    } else {
                        showMessage();
                    }
                    return false;
                }

            });

        }


    }
    public void showMessage() {
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("이 곳의 밀집도");
        builder.setMessage("      사람이 많고, 밀집도가 높습니다");
        builder.setIcon(R.drawable.sorryface);
        builder.setNeutralButton("확인", new DialogInterface.OnClickListener(){
            @Override
            public void onClick(DialogInterface dialog, int which){
                Snackbar.make(textView,"       마스크를 꼭 착용해주세요~~ ", Snackbar.LENGTH_LONG).show();
            }
        });


        AlertDialog dialog = builder.create();
        dialog.show();
    }
    public void showMessage1() {
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("이 곳의 밀집도");
        builder.setMessage("       사람이 적고, 밀집도가 낮습니다");
        builder.setIcon(R.drawable.happyface);
        builder.setNeutralButton("확인", new DialogInterface.OnClickListener(){
            @Override
            public void onClick(DialogInterface dialog, int which){
                Snackbar.make(textView,"       마스크를 꼭 착용해주세요~~", Snackbar.LENGTH_LONG).show();
            }
        });
        AlertDialog dialog = builder.create();
        dialog.show();
    }

    @Override
    public boolean onClick(@NonNull Overlay overlay) {
        return false;
    }
}



