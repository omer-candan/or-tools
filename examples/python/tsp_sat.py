#!/usr/bin/env python3
# Copyright 2010-2022 Google LLC
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Simple travelling salesman problem between cities."""

from ortools.sat.python import cp_model

DISTANCE_MATRIX = [
    [
        0,
        10938,
        4542,
        2835,
        29441,
        2171,
        1611,
        9208,
        9528,
        11111,
        16120,
        22606,
        22127,
        20627,
        21246,
        23387,
        16697,
        33609,
        26184,
        24772,
        22644,
        20655,
        30492,
        23296,
        32979,
        18141,
        19248,
        17129,
        17192,
        15645,
        12658,
        11210,
        12094,
        13175,
        18162,
        4968,
        12308,
        10084,
        13026,
        15056,
    ],
    [
        10938,
        0,
        6422,
        9742,
        18988,
        12974,
        11216,
        19715,
        19004,
        18271,
        25070,
        31971,
        31632,
        30571,
        31578,
        33841,
        27315,
        43964,
        36944,
        35689,
        33569,
        31481,
        41360,
        33760,
        43631,
        28730,
        29976,
        27803,
        28076,
        26408,
        23504,
        22025,
        22000,
        13197,
        14936,
        15146,
        23246,
        20956,
        23963,
        25994,
    ],
    [
        4542,
        6422,
        0,
        3644,
        25173,
        6552,
        5092,
        13584,
        13372,
        13766,
        19805,
        26537,
        26117,
        24804,
        25590,
        27784,
        21148,
        37981,
        30693,
        29315,
        27148,
        25071,
        34943,
        27472,
        37281,
        22389,
        23592,
        21433,
        21655,
        20011,
        17087,
        15612,
        15872,
        11653,
        15666,
        8842,
        16843,
        14618,
        17563,
        19589,
    ],
    [
        2835,
        9742,
        3644,
        0,
        28681,
        3851,
        4341,
        11660,
        12294,
        13912,
        18893,
        25283,
        24777,
        23173,
        23636,
        25696,
        18950,
        35927,
        28233,
        26543,
        24127,
        21864,
        31765,
        24018,
        33904,
        19005,
        20295,
        18105,
        18551,
        16763,
        13958,
        12459,
        12296,
        10370,
        15331,
        5430,
        14044,
        12135,
        14771,
        16743,
    ],
    [
        29441,
        18988,
        25173,
        28681,
        0,
        31590,
        29265,
        37173,
        35501,
        32929,
        40239,
        47006,
        46892,
        46542,
        48112,
        50506,
        44539,
        60103,
        54208,
        53557,
        51878,
        50074,
        59849,
        52645,
        62415,
        47544,
        48689,
        46560,
        46567,
        45086,
        42083,
        40648,
        40971,
        29929,
        28493,
        34015,
        41473,
        38935,
        42160,
        44198,
    ],
    [
        2171,
        12974,
        6552,
        3851,
        31590,
        0,
        3046,
        7856,
        8864,
        11330,
        15411,
        21597,
        21065,
        19382,
        19791,
        21845,
        15099,
        32076,
        24425,
        22848,
        20600,
        18537,
        28396,
        21125,
        30825,
        15975,
        17101,
        14971,
        15104,
        13503,
        10544,
        9080,
        9983,
        13435,
        18755,
        2947,
        10344,
        8306,
        11069,
        13078,
    ],
    [
        1611,
        11216,
        5092,
        4341,
        29265,
        3046,
        0,
        8526,
        8368,
        9573,
        14904,
        21529,
        21085,
        19719,
        20504,
        22713,
        16118,
        32898,
        25728,
        24541,
        22631,
        20839,
        30584,
        23755,
        33278,
        18557,
        19545,
        17490,
        17309,
        15936,
        12881,
        11498,
        12944,
        14711,
        19589,
        5993,
        12227,
        9793,
        12925,
        14967,
    ],
    [
        9208,
        19715,
        13584,
        11660,
        37173,
        7856,
        8526,
        0,
        3248,
        7855,
        8245,
        13843,
        13272,
        11526,
        12038,
        14201,
        7599,
        24411,
        17259,
        16387,
        15050,
        13999,
        23134,
        17899,
        26460,
        12894,
        13251,
        11680,
        10455,
        9997,
        7194,
        6574,
        10678,
        20959,
        26458,
        8180,
        5255,
        2615,
        5730,
        7552,
    ],
    [
        9528,
        19004,
        13372,
        12294,
        35501,
        8864,
        8368,
        3248,
        0,
        4626,
        6598,
        13168,
        12746,
        11567,
        12731,
        15083,
        9120,
        25037,
        18718,
        18433,
        17590,
        16888,
        25630,
        20976,
        29208,
        16055,
        16300,
        14838,
        13422,
        13165,
        10430,
        9813,
        13777,
        22300,
        27564,
        10126,
        8388,
        5850,
        8778,
        10422,
    ],
    [
        11111,
        18271,
        13766,
        13912,
        32929,
        11330,
        9573,
        7855,
        4626,
        0,
        7318,
        14185,
        14005,
        13655,
        15438,
        17849,
        12839,
        27179,
        21947,
        22230,
        21814,
        21366,
        29754,
        25555,
        33535,
        20674,
        20872,
        19457,
        17961,
        17787,
        15048,
        14372,
        18115,
        24280,
        29101,
        13400,
        13008,
        10467,
        13375,
        14935,
    ],
    [
        16120,
        25070,
        19805,
        18893,
        40239,
        15411,
        14904,
        8245,
        6598,
        7318,
        0,
        6939,
        6702,
        6498,
        8610,
        10961,
        7744,
        19889,
        15350,
        16403,
        16975,
        17517,
        24357,
        22176,
        28627,
        18093,
        17672,
        16955,
        14735,
        15510,
        13694,
        13768,
        18317,
        28831,
        34148,
        16326,
        11276,
        9918,
        11235,
        11891,
    ],
    [
        22606,
        31971,
        26537,
        25283,
        47006,
        21597,
        21529,
        13843,
        13168,
        14185,
        6939,
        0,
        793,
        3401,
        5562,
        6839,
        8923,
        13433,
        11264,
        13775,
        15853,
        17629,
        21684,
        22315,
        26411,
        19539,
        18517,
        18636,
        16024,
        17632,
        16948,
        17587,
        22131,
        34799,
        40296,
        21953,
        14739,
        14568,
        14366,
        14002,
    ],
    [
        22127,
        31632,
        26117,
        24777,
        46892,
        21065,
        21085,
        13272,
        12746,
        14005,
        6702,
        793,
        0,
        2608,
        4809,
        6215,
        8151,
        13376,
        10702,
        13094,
        15099,
        16845,
        21039,
        21535,
        25744,
        18746,
        17725,
        17845,
        15232,
        16848,
        16197,
        16859,
        21391,
        34211,
        39731,
        21345,
        14006,
        13907,
        13621,
        13225,
    ],
    [
        20627,
        30571,
        24804,
        23173,
        46542,
        19382,
        19719,
        11526,
        11567,
        13655,
        6498,
        3401,
        2608,
        0,
        2556,
        4611,
        5630,
        13586,
        9157,
        11005,
        12681,
        14285,
        19044,
        18996,
        23644,
        16138,
        15126,
        15240,
        12625,
        14264,
        13736,
        14482,
        18958,
        32292,
        37879,
        19391,
        11621,
        11803,
        11188,
        10671,
    ],
    [
        21246,
        31578,
        25590,
        23636,
        48112,
        19791,
        20504,
        12038,
        12731,
        15438,
        8610,
        5562,
        4809,
        2556,
        0,
        2411,
        4917,
        12395,
        6757,
        8451,
        10292,
        12158,
        16488,
        16799,
        21097,
        14374,
        13194,
        13590,
        10943,
        12824,
        12815,
        13779,
        18042,
        32259,
        37918,
        19416,
        10975,
        11750,
        10424,
        9475,
    ],
    [
        23387,
        33841,
        27784,
        25696,
        50506,
        21845,
        22713,
        14201,
        15083,
        17849,
        10961,
        6839,
        6215,
        4611,
        2411,
        0,
        6760,
        10232,
        4567,
        7010,
        9607,
        12003,
        14846,
        16408,
        19592,
        14727,
        13336,
        14109,
        11507,
        13611,
        14104,
        15222,
        19237,
        34013,
        39703,
        21271,
        12528,
        13657,
        11907,
        10633,
    ],
    [
        16697,
        27315,
        21148,
        18950,
        44539,
        15099,
        16118,
        7599,
        9120,
        12839,
        7744,
        8923,
        8151,
        5630,
        4917,
        6760,
        0,
        16982,
        9699,
        9400,
        9302,
        9823,
        16998,
        14534,
        21042,
        10911,
        10190,
        9900,
        7397,
        8758,
        8119,
        8948,
        13353,
        27354,
        33023,
        14542,
        6106,
        6901,
        5609,
        5084,
    ],
    [
        33609,
        43964,
        37981,
        35927,
        60103,
        32076,
        32898,
        24411,
        25037,
        27179,
        19889,
        13433,
        13376,
        13586,
        12395,
        10232,
        16982,
        0,
        8843,
        12398,
        16193,
        19383,
        16423,
        22583,
        20997,
        22888,
        21194,
        22640,
        20334,
        22636,
        23801,
        25065,
        28675,
        44048,
        49756,
        31426,
        22528,
        23862,
        21861,
        20315,
    ],
    [
        26184,
        36944,
        30693,
        28233,
        54208,
        24425,
        25728,
        17259,
        18718,
        21947,
        15350,
        11264,
        10702,
        9157,
        6757,
        4567,
        9699,
        8843,
        0,
        3842,
        7518,
        10616,
        10666,
        14237,
        15515,
        14053,
        12378,
        13798,
        11537,
        13852,
        15276,
        16632,
        19957,
        35660,
        41373,
        23361,
        14333,
        16125,
        13624,
        11866,
    ],
    [
        24772,
        35689,
        29315,
        26543,
        53557,
        22848,
        24541,
        16387,
        18433,
        22230,
        16403,
        13775,
        13094,
        11005,
        8451,
        7010,
        9400,
        12398,
        3842,
        0,
        3795,
        7014,
        8053,
        10398,
        12657,
        10633,
        8889,
        10569,
        8646,
        10938,
        12906,
        14366,
        17106,
        33171,
        38858,
        21390,
        12507,
        14748,
        11781,
        9802,
    ],
    [
        22644,
        33569,
        27148,
        24127,
        51878,
        20600,
        22631,
        15050,
        17590,
        21814,
        16975,
        15853,
        15099,
        12681,
        10292,
        9607,
        9302,
        16193,
        7518,
        3795,
        0,
        3250,
        8084,
        6873,
        11763,
        6949,
        5177,
        7050,
        5619,
        7730,
        10187,
        11689,
        13792,
        30012,
        35654,
        18799,
        10406,
        12981,
        9718,
        7682,
    ],
    [
        20655,
        31481,
        25071,
        21864,
        50074,
        18537,
        20839,
        13999,
        16888,
        21366,
        17517,
        17629,
        16845,
        14285,
        12158,
        12003,
        9823,
        19383,
        10616,
        7014,
        3250,
        0,
        9901,
        4746,
        12531,
        3737,
        1961,
        4036,
        3588,
        5109,
        7996,
        9459,
        10846,
        27094,
        32690,
        16451,
        8887,
        11624,
        8304,
        6471,
    ],
    [
        30492,
        41360,
        34943,
        31765,
        59849,
        28396,
        30584,
        23134,
        25630,
        29754,
        24357,
        21684,
        21039,
        19044,
        16488,
        14846,
        16998,
        16423,
        10666,
        8053,
        8084,
        9901,
        0,
        9363,
        4870,
        13117,
        11575,
        13793,
        13300,
        15009,
        17856,
        19337,
        20454,
        36551,
        42017,
        26352,
        18403,
        21033,
        17737,
        15720,
    ],
    [
        23296,
        33760,
        27472,
        24018,
        52645,
        21125,
        23755,
        17899,
        20976,
        25555,
        22176,
        22315,
        21535,
        18996,
        16799,
        16408,
        14534,
        22583,
        14237,
        10398,
        6873,
        4746,
        9363,
        0,
        10020,
        5211,
        4685,
        6348,
        7636,
        8010,
        11074,
        12315,
        11926,
        27537,
        32880,
        18634,
        12644,
        15358,
        12200,
        10674,
    ],
    [
        32979,
        43631,
        37281,
        33904,
        62415,
        30825,
        33278,
        26460,
        29208,
        33535,
        28627,
        26411,
        25744,
        23644,
        21097,
        19592,
        21042,
        20997,
        15515,
        12657,
        11763,
        12531,
        4870,
        10020,
        0,
        14901,
        13738,
        15855,
        16118,
        17348,
        20397,
        21793,
        21936,
        37429,
        42654,
        28485,
        21414,
        24144,
        20816,
        18908,
    ],
    [
        18141,
        28730,
        22389,
        19005,
        47544,
        15975,
        18557,
        12894,
        16055,
        20674,
        18093,
        19539,
        18746,
        16138,
        14374,
        14727,
        10911,
        22888,
        14053,
        10633,
        6949,
        3737,
        13117,
        5211,
        14901,
        0,
        1777,
        1217,
        3528,
        2896,
        5892,
        7104,
        7338,
        23517,
        29068,
        13583,
        7667,
        10304,
        7330,
        6204,
    ],
    [
        19248,
        29976,
        23592,
        20295,
        48689,
        17101,
        19545,
        13251,
        16300,
        20872,
        17672,
        18517,
        17725,
        15126,
        13194,
        13336,
        10190,
        21194,
        12378,
        8889,
        5177,
        1961,
        11575,
        4685,
        13738,
        1777,
        0,
        2217,
        2976,
        3610,
        6675,
        8055,
        8965,
        25197,
        30774,
        14865,
        8007,
        10742,
        7532,
        6000,
    ],
    [
        17129,
        27803,
        21433,
        18105,
        46560,
        14971,
        17490,
        11680,
        14838,
        19457,
        16955,
        18636,
        17845,
        15240,
        13590,
        14109,
        9900,
        22640,
        13798,
        10569,
        7050,
        4036,
        13793,
        6348,
        15855,
        1217,
        2217,
        0,
        2647,
        1686,
        4726,
        6000,
        6810,
        23060,
        28665,
        12674,
        6450,
        9094,
        6117,
        5066,
    ],
    [
        17192,
        28076,
        21655,
        18551,
        46567,
        15104,
        17309,
        10455,
        13422,
        17961,
        14735,
        16024,
        15232,
        12625,
        10943,
        11507,
        7397,
        20334,
        11537,
        8646,
        5619,
        3588,
        13300,
        7636,
        16118,
        3528,
        2976,
        2647,
        0,
        2320,
        4593,
        6093,
        8479,
        24542,
        30219,
        13194,
        5301,
        8042,
        4735,
        3039,
    ],
    [
        15645,
        26408,
        20011,
        16763,
        45086,
        13503,
        15936,
        9997,
        13165,
        17787,
        15510,
        17632,
        16848,
        14264,
        12824,
        13611,
        8758,
        22636,
        13852,
        10938,
        7730,
        5109,
        15009,
        8010,
        17348,
        2896,
        3610,
        1686,
        2320,
        0,
        3086,
        4444,
        6169,
        22301,
        27963,
        11344,
        4780,
        7408,
        4488,
        3721,
    ],
    [
        12658,
        23504,
        17087,
        13958,
        42083,
        10544,
        12881,
        7194,
        10430,
        15048,
        13694,
        16948,
        16197,
        13736,
        12815,
        14104,
        8119,
        23801,
        15276,
        12906,
        10187,
        7996,
        17856,
        11074,
        20397,
        5892,
        6675,
        4726,
        4593,
        3086,
        0,
        1501,
        5239,
        20390,
        26101,
        8611,
        2418,
        4580,
        2599,
        3496,
    ],
    [
        11210,
        22025,
        15612,
        12459,
        40648,
        9080,
        11498,
        6574,
        9813,
        14372,
        13768,
        17587,
        16859,
        14482,
        13779,
        15222,
        8948,
        25065,
        16632,
        14366,
        11689,
        9459,
        19337,
        12315,
        21793,
        7104,
        8055,
        6000,
        6093,
        4444,
        1501,
        0,
        4608,
        19032,
        24747,
        7110,
        2860,
        4072,
        3355,
        4772,
    ],
    [
        12094,
        22000,
        15872,
        12296,
        40971,
        9983,
        12944,
        10678,
        13777,
        18115,
        18317,
        22131,
        21391,
        18958,
        18042,
        19237,
        13353,
        28675,
        19957,
        17106,
        13792,
        10846,
        20454,
        11926,
        21936,
        7338,
        8965,
        6810,
        8479,
        6169,
        5239,
        4608,
        0,
        16249,
        21866,
        7146,
        7403,
        8446,
        7773,
        8614,
    ],
    [
        13175,
        13197,
        11653,
        10370,
        29929,
        13435,
        14711,
        20959,
        22300,
        24280,
        28831,
        34799,
        34211,
        32292,
        32259,
        34013,
        27354,
        44048,
        35660,
        33171,
        30012,
        27094,
        36551,
        27537,
        37429,
        23517,
        25197,
        23060,
        24542,
        22301,
        20390,
        19032,
        16249,
        0,
        5714,
        12901,
        21524,
        20543,
        22186,
        23805,
    ],
    [
        18162,
        14936,
        15666,
        15331,
        28493,
        18755,
        19589,
        26458,
        27564,
        29101,
        34148,
        40296,
        39731,
        37879,
        37918,
        39703,
        33023,
        49756,
        41373,
        38858,
        35654,
        32690,
        42017,
        32880,
        42654,
        29068,
        30774,
        28665,
        30219,
        27963,
        26101,
        24747,
        21866,
        5714,
        0,
        18516,
        27229,
        26181,
        27895,
        29519,
    ],
    [
        4968,
        15146,
        8842,
        5430,
        34015,
        2947,
        5993,
        8180,
        10126,
        13400,
        16326,
        21953,
        21345,
        19391,
        19416,
        21271,
        14542,
        31426,
        23361,
        21390,
        18799,
        16451,
        26352,
        18634,
        28485,
        13583,
        14865,
        12674,
        13194,
        11344,
        8611,
        7110,
        7146,
        12901,
        18516,
        0,
        9029,
        7668,
        9742,
        11614,
    ],
    [
        12308,
        23246,
        16843,
        14044,
        41473,
        10344,
        12227,
        5255,
        8388,
        13008,
        11276,
        14739,
        14006,
        11621,
        10975,
        12528,
        6106,
        22528,
        14333,
        12507,
        10406,
        8887,
        18403,
        12644,
        21414,
        7667,
        8007,
        6450,
        5301,
        4780,
        2418,
        2860,
        7403,
        21524,
        27229,
        9029,
        0,
        2747,
        726,
        2749,
    ],
    [
        10084,
        20956,
        14618,
        12135,
        38935,
        8306,
        9793,
        2615,
        5850,
        10467,
        9918,
        14568,
        13907,
        11803,
        11750,
        13657,
        6901,
        23862,
        16125,
        14748,
        12981,
        11624,
        21033,
        15358,
        24144,
        10304,
        10742,
        9094,
        8042,
        7408,
        4580,
        4072,
        8446,
        20543,
        26181,
        7668,
        2747,
        0,
        3330,
        5313,
    ],
    [
        13026,
        23963,
        17563,
        14771,
        42160,
        11069,
        12925,
        5730,
        8778,
        13375,
        11235,
        14366,
        13621,
        11188,
        10424,
        11907,
        5609,
        21861,
        13624,
        11781,
        9718,
        8304,
        17737,
        12200,
        20816,
        7330,
        7532,
        6117,
        4735,
        4488,
        2599,
        3355,
        7773,
        22186,
        27895,
        9742,
        726,
        3330,
        0,
        2042,
    ],
    [
        15056,
        25994,
        19589,
        16743,
        44198,
        13078,
        14967,
        7552,
        10422,
        14935,
        11891,
        14002,
        13225,
        10671,
        9475,
        10633,
        5084,
        20315,
        11866,
        9802,
        7682,
        6471,
        15720,
        10674,
        18908,
        6204,
        6000,
        5066,
        3039,
        3721,
        3496,
        4772,
        8614,
        23805,
        29519,
        11614,
        2749,
        5313,
        2042,
        0,
    ],
]  # yapf: disable


def main():
    """Entry point of the program."""
    num_nodes = len(DISTANCE_MATRIX)
    all_nodes = range(num_nodes)
    print("Num nodes =", num_nodes)

    # Model.
    model = cp_model.CpModel()

    obj_vars = []
    obj_coeffs = []

    # Create the circuit constraint.
    arcs = []
    arc_literals = {}
    for i in all_nodes:
        for j in all_nodes:
            if i == j:
                continue

            lit = model.NewBoolVar("%i follows %i" % (j, i))
            arcs.append([i, j, lit])
            arc_literals[i, j] = lit

            obj_vars.append(lit)
            obj_coeffs.append(DISTANCE_MATRIX[i][j])

    model.AddCircuit(arcs)

    # Minimize weighted sum of arcs. Because this s
    model.Minimize(sum(obj_vars[i] * obj_coeffs[i] for i in range(len(obj_vars))))

    # Solve and print out the solution.
    solver = cp_model.CpSolver()
    solver.parameters.log_search_progress = True
    # To benefit from the linearization of the circuit constraint.
    solver.parameters.linearization_level = 2

    solver.Solve(model)
    print(solver.ResponseStats())

    current_node = 0
    str_route = "%i" % current_node
    route_is_finished = False
    route_distance = 0
    while not route_is_finished:
        for i in all_nodes:
            if i == current_node:
                continue
            if solver.BooleanValue(arc_literals[current_node, i]):
                str_route += " -> %i" % i
                route_distance += DISTANCE_MATRIX[current_node][i]
                current_node = i
                if current_node == 0:
                    route_is_finished = True
                break

    print("Route:", str_route)
    print("Travelled distance:", route_distance)


if __name__ == "__main__":
    main()
