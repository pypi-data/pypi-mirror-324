# kbostadium

* Review and Amenities Information Project for All Korean Baseball Team Stadiums

### USE
```
$ info-sta --help

 Usage: info-sta [OPTIONS] KEYWORD

╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    keyword      TEXT  [default: None] [required]                                                                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --asc     --no-asc             [default: no-asc]                                                                                             │
│ --rcnt                INTEGER  [default: 10]                                                                                                 │
│ --help                         Show this message and exit.                                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

$ info-sta 좌석수 --asc

         구단     좌석수
0   키움 히어로즈  16,670
1   NC 다이노스  17,891
2     KT 위즈  18,700
3    한화 이글스  20,007
4  KIA 타이거즈  20,500
5   롯데 자이언츠  22,758
6   SSG 랜더스  23,000
7    LG 트윈스  23,750
8    두산 베어스  23,750
9   삼성 라이온즈  24,000
```

### Provided Content
* Basic Information by Stadium /  현재 검색 가능 정보 -> (경기장명, 주소, 완공연도, 건축면적, 좌석수)
- not now
* Transportation by Stadium - Directions, Bus/Subway Boarding Locations
* Food and Amenities by Stadium - Types and Locations of Parking Lots, Restaurants, Convenience Stores, Goods Stores, Restrooms, Nursing Rooms, Gate Locations
* Seating by Stadium - Characteristics, Views, Prices, Discount Information, Purchase Locations
* Next Game Recommendations Based on User's Past Visits and Preferences

### DEV
```bash
$ git clone ...
$ pdm venv create
$ source .venv/bin/activate
$ pdm install
$ pytest
```
