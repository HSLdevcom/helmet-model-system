tour_patterns = {
# utility function 1
    0: {
        "- ", : {
            "constant": 0
            , # osiota 1 (vakio) ei ole
            "individual_dummy": {
                "age_50_64 ": -0.305509545 ,
                "age_65_ ": 0.597976527 ,
            }, # osio 3 paattyy
        }, # funktio 1  valmis
# utility function 2
    },
    1: {
        "hw ", : {
            "constant": 0
            , # osiota 1 (vakio) ei ole
            "individual_dummy": {
                "age_18-29 ": 2.306249018 ,
                "age_30_49 ": 2.977241136 ,
                "age_50_64 ": 2.018825449 ,
                "age_65_ ": -1.185980639 ,
            }, # osio 2 paattyy
            "zone": {
                "share_detached_houses ": -0.00591 ,
            }, # osio 3 paattyy
        }, # funktio 2  valmis
# utility function 3
        "hs ", : {
            "constant": 3.308625072
             , # osiota 2 ei ole
            "zone": {
                "share_detached_houses ": -0.00591 ,
            }, # osio 3 paattyy
        }, # funktio 3  valmis
# utility function 4
        "hu ", : {
            "constant": 0
            , # osiota 1 (vakio) ei ole
            "individual_dummy": {
                "age_30_49 ": -1.586979829 ,
                "age_50_64 ": -3.739206239 ,
                "age_65_ ": -3.636471246 ,
            }, # osio 2 paattyy
            "zone": {
                "share_detached_houses ": -0.00591 ,
                "hu_t ": 0.148402259 ,
            }, # osio 3 paattyy
        }, # funktio 4  valmis
# utility function 5
        "hc ", : {
            "constant": 0
            , # osiota 1 (vakio) ei ole
            "individual_dummy": {
                "age_18-29 ": 0.632156675 ,
                "age_30_49 ": 1.106558979 ,
                "age_50_64 ": 0.636516485 ,
                "age_65_ ": 1.250192981 ,
            }, # osio 2 paattyy
            "zone": {
                "share_detached_houses ": -0.00591 ,
            }, # osio 3 paattyy
        }, # funktio 5  valmis
# utility function 6
        "ho ", : {
            "constant": 0.811674639
            , # osio 1 (vakio) paattyy
            "individual_dummy": {
                "age_65_ ": 0.394182783 ,
            }, # osio 2 paattyy
            "zone": {
                "share_detached_houses ": -0.00591 ,
            }, # osio 3 paattyy
        }, # funktio 6  valmis
# utility function 7
    },
    2: {
        "hw-hw ", : {
            "constant": -6.702389265
            , # osio 1 (vakio) paattyy
            "individual_dummy": {
                "age_18-29 ": 2.306249018 ,
                "age_30_49 ": 2.977241136 ,
                "age_50_64 ": 2.018825449 ,
                "age_65_ ": -1.185980639 ,
                "car_users ": 0.647176487 ,
            }, # osio 2 paattyy
            "zone": {
                "ho_w ": 0.249875934 ,
            }, # osio 3 paattyy
        }, # funktio 7  valmis
# utility function 8
        "hw-hu ", : {
            "constant": -8.418852173
            , # osio 1 (vakio) paattyy
            "individual_dummy": {
                "age_18-29 ": 2.306249018 ,
                "age_30_49 ": -1.586979829 ,
                "age_30_49 ": 2.977241136 ,
                "age_50_64 ": -3.739206239 ,
                "age_50_64 ": 2.018825449 ,
                "age_65_ ": -3.636471246 ,
                "age_65_ ": -1.185980639 ,
                "car_users ": 0.647176487 ,
            }, # osio 2 paattyy
            "zone": {
                "hu_t ": 0.176002681 ,
                "ho_w ": 0.249875934 ,
            }, # osio 3 paattyy
        }, # funktio 8  valmis
# utility function 9
        "hw-hc ", : {
            "constant": -5.468303413
            , # osio 1 (vakio) paattyy
            "individual_dummy": {
                "age_18-29 ": 0.632156675 ,
                "age_18-29 ": 2.306249018 ,
                "age_30_49 ": 1.106558979 ,
                "age_30_49 ": 2.977241136 ,
                "age_50_64 ": 0.636516485 ,
                "age_50_64 ": 2.018825449 ,
                "age_65_ ": 1.250192981 ,
                "age_65_ ": -1.185980639 ,
                "car_users ": 0.647176487 ,
            }, # osio 2 paattyy
            "zone": {
                "ho_w ": 0.249875934 ,
            }, # osio 3 paattyy
        }, # funktio 9  valmis
# utility function 10
        "hw-ho ", : {
            "constant": -3.969665707
            , # osio 1 (vakio) paattyy
            "individual_dummy": {
                "age_18-29 ": 2.306249018 ,
                "age_30_49 ": 2.977241136 ,
                "age_50_64 ": 2.018825449 ,
                "age_65_ ": 0.394182783 ,
                "age_65_ ": -1.185980639 ,
                "car_users ": 0.647176487 ,
            }, # osio 2 paattyy
            "zone": {
                "ho_w ": 0.249875934 ,
            }, # osio 3 paattyy
        }, # funktio 10  valmis
# utility function 11
        "hs-hs ", : {
            "constant": -2.189925729
             , # osiota 2 ei ole
            "zone": {
                "ho_w ": 0.249875934 ,
            }, # osio 3 paattyy
        }, # funktio 11  valmis
# utility function 12
        "hs-hc ", : {
            "constant": -0.932031836
            , # osio 1 (vakio) paattyy
            "individual_dummy": {
                "age_18-29 ": 0.632156675 ,
                "age_30_49 ": 1.106558979 ,
                "age_50_64 ": 0.636516485 ,
                "age_65_ ": 1.250192981 ,
            }, # osio 2 paattyy
            "zone": {
                "ho_w ": 0.249875934 ,
            }, # osio 3 paattyy
        }, # funktio 12  valmis
# utility function 13
        "hs-ho ", : {
            "constant": 1.040646615
            , # osio 1 (vakio) paattyy
            "individual_dummy": {
                "age_65_ ": 0.394182783 ,
            }, # osio 2 paattyy
            "zone": {
                "ho_w ": 0.249875934 ,
            }, # osio 3 paattyy
        }, # funktio 13  valmis
# utility function 14
        "hu-hc ", : {
            "constant": -5.264912587
            , # osio 1 (vakio) paattyy
            "individual_dummy": {
                "age_18-29 ": 0.632156675 ,
                "age_30_49 ": 1.106558979 ,
                "age_30_49 ": -1.586979829 ,
                "age_50_64 ": 0.636516485 ,
                "age_50_64 ": -3.739206239 ,
                "age_65_ ": 1.250192981 ,
                "age_65_ ": -3.636471246 ,
                "car_users ": 0.647176487 ,
            }, # osio 2 paattyy
            "zone": {
                "hu_t ": 0.176002681 ,
                "ho_w ": 0.249875934 ,
            }, # osio 3 paattyy
        }, # funktio 14  valmis
# utility function 15
        "hu-ho ", : {
            "constant": -4.133565561
            , # osio 1 (vakio) paattyy
            "individual_dummy": {
                "age_30_49 ": -1.586979829 ,
                "age_50_64 ": -3.739206239 ,
                "age_65_ ": 0.394182783 ,
                "age_65_ ": -3.636471246 ,
                "car_users ": 0.647176487 ,
            }, # osio 2 paattyy
            "zone": {
                "hu_t ": 0.176002681 ,
                "ho_w ": 0.249875934 ,
            }, # osio 3 paattyy
        }, # funktio 15  valmis
# utility function 16
        "hc-hc ", : {
            "constant": -4.347727916
            , # osio 1 (vakio) paattyy
            "individual_dummy": {
                "age_18-29 ": 0.632156675 ,
                "age_30_49 ": 1.106558979 ,
                "age_50_64 ": 0.636516485 ,
                "age_65_ ": 1.250192981 ,
                "car_users ": 0.647176487 ,
            }, # osio 2 paattyy
            "zone": {
                "ho_w ": 0.249875934 ,
            }, # osio 3 paattyy
        }, # funktio 16  valmis
# utility function 17
        "hc-ho ", : {
            "constant": -3.615413138
            , # osio 1 (vakio) paattyy
            "individual_dummy": {
                "age_18-29 ": 0.632156675 ,
                "age_30_49 ": 1.106558979 ,
                "age_50_64 ": 0.636516485 ,
                "age_65_ ": 1.250192981 ,
                "age_65_ ": 0.394182783 ,
                "car_users ": 0.647176487 ,
            }, # osio 2 paattyy
            "zone": {
                "ho_w ": 0.249875934 ,
            }, # osio 3 paattyy
        }, # funktio 17  valmis
# utility function 18
        "ho-ho ", : {
            "constant": -2.954069138
            , # osio 1 (vakio) paattyy
            "individual_dummy": {
                "age_65_ ": 0.394182783 ,
                "car_users ": 0.647176487 ,
            }, # osio 2 paattyy
            "zone": {
                "ho_w ": 0.249875934 ,
            }, # osio 3 paattyy
        }, # funktio 18  valmis
# utility function 19
    },
    3: {
        "hw-hw-ho ", : {
            "constant": -7.640316015
            , # osio 1 (vakio) paattyy
            "individual_dummy": {
                "age_18-29 ": 2.306249018 ,
                "age_30_49 ": 2.977241136 ,
                "age_50_64 ": 2.018825449 ,
                "age_65_ ": 0.394182783 ,
                "age_65_ ": -1.185980639 ,
                "car_users ": 1.492056593 ,
            }, # osio 3 paattyy
        }, # funktio 19  valmis
# utility function 20
        "hw-hc-hc ", : {
            "constant": -6.996908123
            , # osio 1 (vakio) paattyy
            "individual_dummy": {
                "age_18-29 ": 0.632156675 ,
                "age_18-29 ": 2.306249018 ,
                "age_30_49 ": 1.106558979 ,
                "age_30_49 ": 2.977241136 ,
                "age_50_64 ": 0.636516485 ,
                "age_50_64 ": 2.018825449 ,
                "age_65_ ": 1.250192981 ,
                "age_65_ ": -1.185980639 ,
                "car_users ": 1.492056593 ,
            }, # osio 3 paattyy
        }, # funktio 20  valmis
# utility function 21
        "hw-hc-ho ", : {
            "constant": -6.28085759
            , # osio 1 (vakio) paattyy
            "individual_dummy": {
                "age_18-29 ": 0.632156675 ,
                "age_18-29 ": 2.306249018 ,
                "age_30_49 ": 1.106558979 ,
                "age_30_49 ": 2.977241136 ,
                "age_50_64 ": 0.636516485 ,
                "age_50_64 ": 2.018825449 ,
                "age_65_ ": 1.250192981 ,
                "age_65_ ": 0.394182783 ,
                "age_65_ ": -1.185980639 ,
                "car_users ": 1.492056593 ,
            }, # osio 3 paattyy
        }, # funktio 21  valmis
# utility function 22
        "hw-ho-ho ", : {
            "constant": -5.143814369
            , # osio 1 (vakio) paattyy
            "individual_dummy": {
                "age_18-29 ": 2.306249018 ,
                "age_30_49 ": 2.977241136 ,
                "age_50_64 ": 2.018825449 ,
                "age_65_ ": 0.394182783 ,
                "age_65_ ": -1.185980639 ,
                "car_users ": 1.492056593 ,
            }, # osio 3 paattyy
        }, # funktio 22  valmis
# utility function 23
        "hs-hc-ho ", : {
            "constant": -1.110080901
            , # osio 1 (vakio) paattyy
            "individual_dummy": {
                "age_18-29 ": 0.632156675 ,
                "age_30_49 ": 1.106558979 ,
                "age_50_64 ": 0.636516485 ,
                "age_65_ ": 1.250192981 ,
                "age_65_ ": 0.394182783 ,
            }, # osio 2 paattyy
            "zone": {
                "ho_w ": 0.0258 ,
            }, # osio 3 paattyy
        }, # funktio 23  valmis
# utility function 24
        "hs-ho-ho ", : {
            "constant": 0
            , # osiota 1 (vakio) ei ole
            "individual_dummy": {
                "age_65_ ": 0.394182783 ,
            }, # osio 2 paattyy
            "zone": {
                "ho_w ": 0.0258 ,
            }, # osio 3 paattyy
        }, # funktio 24  valmis
# utility function 25
        "hu-hc-ho ", : {
            "constant": -11.75180816
            , # osio 1 (vakio) paattyy
            "individual_dummy": {
                "age_18-29 ": 0.632156675 ,
                "age_30_49 ": 1.106558979 ,
                "age_30_49 ": -1.586979829 ,
                "age_50_64 ": 0.636516485 ,
                "age_50_64 ": -3.739206239 ,
                "age_65_ ": 1.250192981 ,
                "age_65_ ": 0.394182783 ,
                "age_65_ ": -3.636471246 ,
                "car_users ": 1.492056593 ,
            }, # osio 2 paattyy
            "zone": {
                "hu_t ": 0.829445548 ,
                "ho_w ": 0.0258 ,
            }, # osio 3 paattyy
        }, # funktio 25  valmis
# utility function 26
        "hu-ho-ho ", : {
            "constant": -11.34272983
            , # osio 1 (vakio) paattyy
            "individual_dummy": {
                "age_30_49 ": -1.586979829 ,
                "age_50_64 ": -3.739206239 ,
                "age_65_ ": 0.394182783 ,
                "age_65_ ": -3.636471246 ,
                "car_users ": 1.492056593 ,
            }, # osio 2 paattyy
            "zone": {
                "hu_t ": 0.829445548 ,
                "ho_w ": 0.0258 ,
            }, # osio 3 paattyy
        }, # funktio 26  valmis
# utility function 27
        "hc-hc-hc ", : {
            "constant": -5.575050535
            , # osio 1 (vakio) paattyy
            "individual_dummy": {
                "age_18-29 ": 0.632156675 ,
                "age_30_49 ": 1.106558979 ,
                "age_50_64 ": 0.636516485 ,
                "age_65_ ": 1.250192981 ,
                "car_users ": 1.492056593 ,
            }, # osio 2 paattyy
            "zone": {
                "ho_w ": 0.0258 ,
            }, # osio 3 paattyy
        }, # funktio 27  valmis
# utility function 28
        "hc-hc-ho ", : {
            "constant": -4.709369964
            , # osio 1 (vakio) paattyy
            "individual_dummy": {
                "age_18-29 ": 0.632156675 ,
                "age_30_49 ": 1.106558979 ,
                "age_50_64 ": 0.636516485 ,
                "age_65_ ": 1.250192981 ,
                "age_65_ ": 0.394182783 ,
                "car_users ": 1.492056593 ,
            }, # osio 2 paattyy
            "zone": {
                "ho_w ": 0.0258 ,
            }, # osio 3 paattyy
        }, # funktio 28  valmis
# utility function 29
        "hc-ho-ho ", : {
            "constant": -4.115616267
            , # osio 1 (vakio) paattyy
            "individual_dummy": {
                "age_18-29 ": 0.632156675 ,
                "age_30_49 ": 1.106558979 ,
                "age_50_64 ": 0.636516485 ,
                "age_65_ ": 1.250192981 ,
                "age_65_ ": 0.394182783 ,
                "car_users ": 1.492056593 ,
            }, # osio 2 paattyy
            "zone": {
                "ho_w ": 0.0258 ,
            }, # osio 3 paattyy
        }, # funktio 29  valmis
# utility function 30
        "ho-ho-ho ", : {
            "constant": -4.110394781
            , # osio 1 (vakio) paattyy
            "individual_dummy": {
                "age_65_ ": 0.394182783 ,
                "car_users ": 1.492056593 ,
            }, # osio 2 paattyy
            "zone": {
                "ho_w ": 0.0258 ,
            }, # osio 3 paattyy
        }, # funktio 30  valmis
# utility function 31
    },
    4: {
        "hw-hc-hc-ho ", : {
            "constant": -8.782904966
            , # osio 1 (vakio) paattyy
            "individual_dummy": {
                "age_18-29 ": 0.632156675 ,
                "age_18-29 ": 2.306249018 ,
                "age_30_49 ": 1.106558979 ,
                "age_30_49 ": 2.977241136 ,
                "age_50_64 ": 0.636516485 ,
                "age_50_64 ": 2.018825449 ,
                "age_65_ ": 1.250192981 ,
                "age_65_ ": 0.394182783 ,
                "age_65_ ": -1.185980639 ,
                "car_users ": 1.544612164 ,
            }, # osio 2 paattyy
            "zone": {
                "share_detached_houses ": -0.00805 ,
            }, # osio 3 paattyy
        }, # funktio 31  valmis
# utility function 32
        "hw-hc-ho-ho ", : {
            "constant": -7.819600775
            , # osio 1 (vakio) paattyy
            "individual_dummy": {
                "age_18-29 ": 0.632156675 ,
                "age_18-29 ": 2.306249018 ,
                "age_30_49 ": 1.106558979 ,
                "age_30_49 ": 2.977241136 ,
                "age_50_64 ": 0.636516485 ,
                "age_50_64 ": 2.018825449 ,
                "age_65_ ": 1.250192981 ,
                "age_65_ ": 0.394182783 ,
                "age_65_ ": -1.185980639 ,
                "car_users ": 1.544612164 ,
            }, # osio 2 paattyy
            "zone": {
                "share_detached_houses ": -0.00805 ,
            }, # osio 3 paattyy
        }, # funktio 32  valmis
# utility function 33
        "hw-ho-ho-ho ", : {
            "constant": -6.323991971
            , # osio 1 (vakio) paattyy
            "individual_dummy": {
                "age_18-29 ": 2.306249018 ,
                "age_30_49 ": 2.977241136 ,
                "age_50_64 ": 2.018825449 ,
                "age_65_ ": 0.394182783 ,
                "age_65_ ": -1.185980639 ,
                "car_users ": 1.544612164 ,
            }, # osio 2 paattyy
            "zone": {
                "share_detached_houses ": -0.00805 ,
            }, # osio 3 paattyy
        }, # funktio 33  valmis
# utility function 34
        "hc-hc-hc-hc ", : {
            "constant": -6.56383811
            , # osio 1 (vakio) paattyy
            "individual_dummy": {
                "age_18-29 ": 0.632156675 ,
                "age_30_49 ": 1.106558979 ,
                "age_50_64 ": 0.636516485 ,
                "age_65_ ": 1.250192981 ,
                "car_users ": 1.544612164 ,
            }, # osio 2 paattyy
            "zone": {
                "share_detached_houses ": -0.00805 ,
            }, # osio 3 paattyy
        }, # funktio 34  valmis
# utility function 35
        "hc-hc-hc-ho ", : {
            "constant": -6.280534875
            , # osio 1 (vakio) paattyy
            "individual_dummy": {
                "age_18-29 ": 0.632156675 ,
                "age_30_49 ": 1.106558979 ,
                "age_50_64 ": 0.636516485 ,
                "age_65_ ": 1.250192981 ,
                "age_65_ ": 0.394182783 ,
                "car_users ": 1.544612164 ,
            }, # osio 2 paattyy
            "zone": {
                "share_detached_houses ": -0.00805 ,
            }, # osio 3 paattyy
        }, # funktio 35  valmis
# utility function 36
        "hc-hc-ho-ho ", : {
            "constant": -5.728407971
            , # osio 1 (vakio) paattyy
            "individual_dummy": {
                "age_18-29 ": 0.632156675 ,
                "age_30_49 ": 1.106558979 ,
                "age_50_64 ": 0.636516485 ,
                "age_65_ ": 1.250192981 ,
                "age_65_ ": 0.394182783 ,
                "car_users ": 1.544612164 ,
            }, # osio 2 paattyy
            "zone": {
                "share_detached_houses ": -0.00805 ,
            }, # osio 3 paattyy
        }, # funktio 36  valmis
# utility function 37
        "hc-ho-ho-ho ", : {
            "constant": -5.1676642
            , # osio 1 (vakio) paattyy
            "individual_dummy": {
                "age_18-29 ": 0.632156675 ,
                "age_30_49 ": 1.106558979 ,
                "age_50_64 ": 0.636516485 ,
                "age_65_ ": 1.250192981 ,
                "age_65_ ": 0.394182783 ,
                "car_users ": 1.544612164 ,
            }, # osio 2 paattyy
            "zone": {
                "share_detached_houses ": -0.00805 ,
            }, # osio 3 paattyy
        }, # funktio 37  valmis
# utility function 38
        "ho-ho-ho-ho ", : {
            "constant": -4.892323651
            , # osio 1 (vakio) paattyy
            "individual_dummy": {
                "age_65_ ": 0.394182783 ,
                "car_users ": 1.544612164 ,
            }, # osio 2 paattyy
            "zone": {
                "share_detached_houses ": -0.00805 ,
            }, # osio 3 paattyy
        }, # funktio 38  valmis
    }, # 4+ matkaa valmis
}, # koko kaava valmis
