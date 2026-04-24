COMMON_SCORE_TEMPLATES = {
    "攻撃力型": {
        "会心率": 2.0,
        "会心ダメージ": 1.0,
        "攻撃%": 1.0,
        "HP%": 0.0,
        "防御%": 0.0,
        "元素熟知": 0.0,
        "元素チャージ効率": 0.0
    },
    "HP型": {
        "会心率": 2.0,
        "会心ダメージ": 1.0,
        "攻撃%": 0.0,
        "HP%": 1.0,
        "防御%": 0.0,
        "元素熟知": 0.0,
        "元素チャージ効率": 0.0
    },
    "防御力型": {
        "会心率": 2.0,
        "会心ダメージ": 1.0,
        "攻撃%": 0.0,
        "HP%": 0.0,
        "防御%": 1.0,
        "元素熟知": 0.0,
        "元素チャージ効率": 0.0
    },
    "熟知型": {
        "会心率": 2.0,
        "会心ダメージ": 1.0,
        "攻撃%": 0.0,
        "HP%": 0.0,
        "防御%": 0.0,
        "元素熟知": 0.25,
        "元素チャージ効率": 0.0
    },
    "チャージ型": {
        "会心率": 2.0,
        "会心ダメージ": 1.0,
        "攻撃%": 0.0,
        "HP%": 0.0,
        "防御%": 0.0,
        "元素熟知": 0.0,
        "元素チャージ効率": 1.0
    }
}
character_builds = {
    "アルレッキーノ": {
        "element": "炎",
        "weapon": "長柄武器",
        "builds": {
            "アタッカー": {
                "fixed_mainstats": {
                    "花": "HP",
                    "羽": "攻撃力"
                },
                "mainstat_options": {
                    "時計": ["攻撃%"],
                    "杯": ["炎ダメージ"],
                    "冠": ["会心率", "会心ダメージ"]
                },
                "score_weight_options": COMMON_SCORE_TEMPLATES,
                "default_score_mode": "攻撃力型",
                "elixir_fixed_substats": {
                    "花": ["会心率", "会心ダメージ"],
                    "羽": ["会心率", "会心ダメージ"],
                    "時計": ["会心率", "会心ダメージ"],
                    "杯": ["会心率", "会心ダメージ"],
                    "冠": ["会心率", "会心ダメージ"]
                },
                "default_target_score": 180
            }
        }
    },

"フリーナ": {
    "element": "水",
    "weapon": "片手剣",
    "builds": {
        "サポート": {
            "fixed_mainstats": {
                "花": "HP",
                "羽": "攻撃力"
            },
            "mainstat_options": {
                "時計": ["HP%", "元素チャージ効率"],
                "杯": ["HP%", "水ダメージ"],
                "冠": ["会心率", "会心ダメージ", "HP%"]
            },
            "score_weight_options": COMMON_SCORE_TEMPLATES,
            "default_score_mode": "HP型",
            "elixir_fixed_substats": {
                "花": ["会心率", "会心ダメージ"],
                "羽": ["会心率", "会心ダメージ"],
                "時計": ["会心率", "会心ダメージ"],
                "杯": ["会心率", "会心ダメージ"],
                "冠": ["会心率", "会心ダメージ"]
            },
            "default_target_score": 180,

            "damage_preview": {
                "stat_type": "HP",

                "base_hp": 15307.39,
                "base_atk": 243.96,
                "base_def": 695.54,

                "ascension_stat": {
                    "type": "会心率",
                    "value": 19.2
                },

                "weapon_base_stat": 542,
                "weapon_sub_stat": {
                    "会心ダメージ": 88.2
                },

                "base_crit_rate": 5.0,
                "base_crit_damage": 50.0,

                "extra_stats": {
                    "HP%": 0.0,
                    "会心率": 0.0,
                    "会心ダメージ": 0.0,
                    "元素チャージ効率": 0.0,
                    "元素熟知": 0.0
                },

                "elemental_bonus_type": "水ダメージ",

                "default_enemy": {
                    "name": "ヒルチャール",
                    "level": 100,
                    "resistance": 10.0
                }
            }
        }
    },

    "クロリンデ": {
        "element": "雷",
        "weapon": "片手剣",
        "builds": {
            "アタッカー": {
                "fixed_mainstats": {
                    "花": "HP",
                    "羽": "攻撃力"
                },
                "mainstat_options": {
                    "時計": ["攻撃%"],
                    "杯": ["雷ダメージ"],
                    "冠": ["会心率", "会心ダメージ"]
                },
                "score_weight_options": COMMON_SCORE_TEMPLATES,
                "default_score_mode": "攻撃力型",
                "elixir_fixed_substats": {
                    "花": ["会心率", "会心ダメージ"],
                    "羽": ["会心率", "会心ダメージ"],
                    "時計": ["会心率", "会心ダメージ"],
                    "杯": ["会心率", "会心ダメージ"],
                    "冠": ["会心率", "会心ダメージ"]
                },
                "default_target_score": 180
            }
        }
    },

    "リオセスリ": {
        "element": "氷",
        "weapon": "法器",
        "builds": {
            "アタッカー": {
                "fixed_mainstats": {
                    "花": "HP",
                    "羽": "攻撃力"
                },
                "mainstat_options": {
                    "時計": ["攻撃%"],
                    "杯": ["氷ダメージ"],
                    "冠": ["会心率", "会心ダメージ"]
                },
                "score_weight_options": COMMON_SCORE_TEMPLATES,
                "default_score_mode": "攻撃力型",
                "elixir_fixed_substats": {
                    "花": ["会心率", "会心ダメージ"],
                    "羽": ["会心率", "会心ダメージ"],
                    "時計": ["会心率", "会心ダメージ"],
                    "杯": ["会心率", "会心ダメージ"],
                    "冠": ["会心率", "会心ダメージ"]
                },
                "default_target_score": 200
            }
        }
    },

    "閑雲": {
        "element": "風",
        "weapon": "法器",
        "builds": {
            "サポート": {
                "fixed_mainstats": {
                    "花": "HP",
                    "羽": "攻撃力"
                },
                "mainstat_options": {
                    "時計": ["攻撃%", "元素チャージ効率"],
                    "杯": ["攻撃%"],
                    "冠": ["攻撃%", "治療効果"]
                },
                "score_weight_options": COMMON_SCORE_TEMPLATES,
                "default_score_mode": "攻撃力型",
                "elixir_fixed_substats": {
                    "花": ["攻撃%", "元素チャージ効率"],
                    "羽": ["攻撃%", "元素チャージ効率"],
                    "時計": ["攻撃%", "元素チャージ効率"],
                    "杯": ["攻撃%", "元素チャージ効率"],
                    "冠": ["攻撃%", "元素チャージ効率"]
                },
                "default_target_score": 180
            }
        }
    },

    "ナヴィア": {
        "element": "岩",
        "weapon": "両手剣",
        "builds": {
            "アタッカー": {
                "fixed_mainstats": {
                    "花": "HP",
                    "羽": "攻撃力"
                },
                "mainstat_options": {
                    "時計": ["攻撃%"],
                    "杯": ["岩ダメージ"],
                    "冠": ["会心率", "会心ダメージ"]
                },
                "score_weight_options": COMMON_SCORE_TEMPLATES,
                "default_score_mode": "攻撃力型",
                "elixir_fixed_substats": {
                    "花": ["会心率", "会心ダメージ"],
                    "羽": ["会心率", "会心ダメージ"],
                    "時計": ["会心率", "会心ダメージ"],
                    "杯": ["会心率", "会心ダメージ"],
                    "冠": ["会心率", "会心ダメージ"]
                },
                "default_target_score": 180
            }
        }
    },

    "アルハイゼン": {
        "element": "草",
        "weapon": "片手剣",
        "builds": {
            "アタッカー": {
                "fixed_mainstats": {
                    "花": "HP",
                    "羽": "攻撃力"
                },
                "mainstat_options": {
                    "時計": ["元素熟知", "攻撃%"],
                    "杯": ["草ダメージ", "元素熟知"],
                    "冠": ["会心率", "会心ダメージ"]
                },
                "score_weight_options": COMMON_SCORE_TEMPLATES,
                "default_score_mode": "熟知型",
                "elixir_fixed_substats": {
                    "花": ["会心率", "会心ダメージ"],
                    "羽": ["会心率", "会心ダメージ"],
                    "時計": ["会心率", "会心ダメージ"],
                    "杯": ["会心率", "会心ダメージ"],
                    "冠": ["会心率", "会心ダメージ"]
                },
                "default_target_score": 180
            }
        }
    },
"ベネット": {
    "element": "炎",
    "weapon": "片手剣",
    "builds": {
        "サポート": {
            "fixed_mainstats": {
                "花": "HP",
                "羽": "攻撃力"
            },
            "mainstat_options": {
                "時計": ["元素チャージ効率", "HP%"],
                "杯": ["HP%", "炎ダメージ"],
                "冠": ["治療効果", "会心率", "会心ダメージ", "HP%"]
            },
            "score_weight_options": COMMON_SCORE_TEMPLATES,
            "default_score_mode": "チャージ型",
            "elixir_fixed_substats": {
                "花": ["元素チャージ効率", "HP%"],
                "羽": ["元素チャージ効率", "HP%"],
                "時計": ["会心率", "会心ダメージ"],
                "杯": ["会心率", "会心ダメージ"],
                "冠": ["元素チャージ効率", "HP%"]
            },
            "default_target_score": 160
        }
    }
},

"ヌヴィレット": {
    "element": "水",
    "weapon": "法器",
    "builds": {
        "アタッカー": {
            "fixed_mainstats": {
                "花": "HP",
                "羽": "攻撃力"
            },
            "mainstat_options": {
                "時計": ["HP%"],
                "杯": ["水ダメージ", "HP%"],
                "冠": ["会心率", "会心ダメージ", "HP%"]
            },
            "score_weight_options": COMMON_SCORE_TEMPLATES,
            "default_score_mode": "HP型",
            "elixir_fixed_substats": {
                "花": ["会心率", "会心ダメージ"],
                "羽": ["会心率", "会心ダメージ"],
                "時計": ["会心率", "会心ダメージ"],
                "杯": ["会心率", "会心ダメージ"],
                "冠": ["会心率", "会心ダメージ"]
            },
            "default_target_score": 180
        }
    }
},

"夜蘭": {
    "element": "水",
    "weapon": "弓",
    "builds": {
        "サブアタッカー": {
            "fixed_mainstats": {
                "花": "HP",
                "羽": "攻撃力"
            },
            "mainstat_options": {
                "時計": ["HP%", "元素チャージ効率"],
                "杯": ["水ダメージ", "HP%"],
                "冠": ["会心率", "会心ダメージ", "HP%"]
            },
            "score_weight_options": COMMON_SCORE_TEMPLATES,
            "default_score_mode": "HP型",
            "elixir_fixed_substats": {
                "花": ["会心率", "会心ダメージ"],
                "羽": ["会心率", "会心ダメージ"],
                "時計": ["会心率", "会心ダメージ"],
                "杯": ["会心率", "会心ダメージ"],
                "冠": ["会心率", "会心ダメージ"]
            },
            "default_target_score": 180
        }
    }
},

"雷電将軍": {
    "element": "雷",
    "weapon": "長柄武器",
    "builds": {
        "アタッカー": {
            "fixed_mainstats": {
                "花": "HP",
                "羽": "攻撃力"
            },
            "mainstat_options": {
                "時計": ["元素チャージ効率", "攻撃%"],
                "杯": ["雷ダメージ", "攻撃%"],
                "冠": ["会心率", "会心ダメージ"]
            },
            "score_weight_options": COMMON_SCORE_TEMPLATES,
            "default_score_mode": "チャージ型",
            "elixir_fixed_substats": {
                "花": ["会心率", "会心ダメージ"],
                "羽": ["会心率", "会心ダメージ"],
                "時計": ["会心率", "会心ダメージ"],
                "杯": ["会心率", "会心ダメージ"],
                "冠": ["会心率", "会心ダメージ"]
            },
            "default_target_score": 180
        }
    }
},

"フィッシュル": {
    "element": "雷",
    "weapon": "弓",
    "builds": {
        "サブアタッカー": {
            "fixed_mainstats": {
                "花": "HP",
                "羽": "攻撃力"
            },
            "mainstat_options": {
                "時計": ["攻撃%", "元素熟知"],
                "杯": ["雷ダメージ", "攻撃%"],
                "冠": ["会心率", "会心ダメージ"]
            },
            "score_weight_options": COMMON_SCORE_TEMPLATES,
            "default_score_mode": "攻撃力型",
            "elixir_fixed_substats": {
                "花": ["会心率", "会心ダメージ"],
                "羽": ["会心率", "会心ダメージ"],
                "時計": ["会心率", "会心ダメージ"],
                "杯": ["会心率", "会心ダメージ"],
                "冠": ["会心率", "会心ダメージ"]
            },
            "default_target_score": 170
        }
    }
},

"神里綾華": {
    "element": "氷",
    "weapon": "片手剣",
    "builds": {
        "アタッカー": {
            "fixed_mainstats": {
                "花": "HP",
                "羽": "攻撃力"
            },
            "mainstat_options": {
                "時計": ["攻撃%"],
                "杯": ["氷ダメージ"],
                "冠": ["会心率", "会心ダメージ", "攻撃%"]
            },
            "score_weight_options": COMMON_SCORE_TEMPLATES,
            "default_score_mode": "攻撃力型",
            "elixir_fixed_substats": {
                "花": ["会心率", "会心ダメージ"],
                "羽": ["会心率", "会心ダメージ"],
                "時計": ["会心率", "会心ダメージ"],
                "杯": ["会心率", "会心ダメージ"],
                "冠": ["会心率", "会心ダメージ"]
            },
            "default_target_score": 190
        }
    }
},

"エスコフィエ": {
    "element": "氷",
    "weapon": "長柄武器",
    "builds": {
        "サポート": {
            "fixed_mainstats": {
                "花": "HP",
                "羽": "攻撃力"
            },
            "mainstat_options": {
                "時計": ["攻撃%", "元素チャージ効率"],
                "杯": ["氷ダメージ", "攻撃%"],
                "冠": ["会心率", "会心ダメージ", "攻撃%"]
            },
            "score_weight_options": COMMON_SCORE_TEMPLATES,
            "default_score_mode": "攻撃力型",
            "elixir_fixed_substats": {
                "花": ["攻撃%", "元素チャージ効率"],
                "羽": ["攻撃%", "元素チャージ効率"],
                "時計": ["会心率", "会心ダメージ"],
                "杯": ["会心率", "会心ダメージ"],
                "冠": ["会心率", "会心ダメージ"]
            },
            "default_target_score": 170
        }
    }
},

"楓原万葉": {
    "element": "風",
    "weapon": "片手剣",
    "builds": {
        "サポート": {
            "fixed_mainstats": {
                "花": "HP",
                "羽": "攻撃力"
            },
            "mainstat_options": {
                "時計": ["元素熟知", "元素チャージ効率"],
                "杯": ["元素熟知"],
                "冠": ["元素熟知"]
            },
            "score_weight_options": COMMON_SCORE_TEMPLATES,
            "default_score_mode": "熟知型",
            "elixir_fixed_substats": {
                "花": ["元素熟知", "元素チャージ効率"],
                "羽": ["元素熟知", "元素チャージ効率"],
                "時計": ["会心率", "元素チャージ効率"],
                "杯": ["会心率", "元素チャージ効率"],
                "冠": ["会心率", "元素チャージ効率"]
            },
            "default_target_score": 160
        }
    }
},
"ファルカ": {
    "element": "風",
    "weapon": "両手剣",
    "builds": {
        "アタッカー": {
            "fixed_mainstats": {
                "花": "HP",
                "羽": "攻撃力"
            },
            "mainstat_options": {
                "時計": ["攻撃%",],
                "杯": ["攻撃%", "炎ダメージ"],
                "冠": ["攻撃%", "会心率", "会心ダメージ"]
            },
            "score_weight_options": COMMON_SCORE_TEMPLATES,
            "default_score_mode": "攻撃力型",
            "elixir_fixed_substats": {
                "花": ["会心率", "会心ダメージ"],
                "羽": ["会心率", "会心ダメージ"],
                "時計": ["会心率", "会心ダメージ"],
                "杯": ["会心率", "会心ダメージ"],
                "冠": ["会心率", "会心ダメージ"]
            },
            "default_target_score": 160
        }
    }
},
"荒瀧一斗": {
    "element": "岩",
    "weapon": "両手剣",
    "builds": {
        "アタッカー": {
            "fixed_mainstats": {
                "花": "HP",
                "羽": "攻撃力"
            },
            "mainstat_options": {
                "時計": ["防御%"],
                "杯": ["岩ダメージ", "防御%"],
                "冠": ["会心率", "会心ダメージ", "防御%"]
            },
            "score_weight_options": COMMON_SCORE_TEMPLATES,
            "default_score_mode": "防御力型",
            "elixir_fixed_substats": {
                "花": ["会心率", "会心ダメージ"],
                "羽": ["会心率", "会心ダメージ"],
                "時計": ["会心率", "会心ダメージ"],
                "杯": ["会心率", "会心ダメージ"],
                "冠": ["会心率", "会心ダメージ"]
            },
            "default_target_score": 180
        }
    }
},
"シロネン": {
    "element": "岩",
    "weapon": "片手剣",
    "builds": {
        "サポート": {
            "fixed_mainstats": {
                "花": "HP",
                "羽": "攻撃力"
            },
            "mainstat_options": {
                "時計": ["防御%", "元素チャージ効率"],
                "杯": ["防御%", "岩ダメージ"],
                "冠": ["防御%", "会心率", "会心ダメージ"]
            },
            "score_weight_options": COMMON_SCORE_TEMPLATES,
            "default_score_mode": "防御力型",
            "elixir_fixed_substats": {
                "花": ["防御%", "元素チャージ効率"],
                "羽": ["防御%", "元素チャージ効率"],
                "時計": ["会心率", "会心ダメージ"],
                "杯": ["会心率", "会心ダメージ"],
                "冠": ["会心率", "会心ダメージ"]
            },
            "default_target_score": 170
        }
    }
},

"ナヒーダ": {
    "element": "草",
    "weapon": "法器",
    "builds": {
        "サポート": {
            "fixed_mainstats": {
                "花": "HP",
                "羽": "攻撃力"
            },
            "mainstat_options": {
                "時計": ["元素熟知"],
                "杯": ["元素熟知", "草ダメージ"],
                "冠": ["元素熟知", "会心率", "会心ダメージ"]
            },
            "score_weight_options": COMMON_SCORE_TEMPLATES,
            "default_score_mode": "熟知型",
            "elixir_fixed_substats": {
                "花": ["元素熟知", "会心率"],
                "羽": ["元素熟知", "会心率"],
                "時計": ["元素熟知", "会心率"],
                "杯": ["元素熟知", "会心率"],
                "冠": ["元素熟知", "会心率"]
            },
            "default_target_score": 170
        }
    }
},

"キィニチ": {
    "element": "草",
    "weapon": "両手剣",
    "builds": {
        "アタッカー": {
            "fixed_mainstats": {
                "花": "HP",
                "羽": "攻撃力"
            },
            "mainstat_options": {
                "時計": ["攻撃%", "元素熟知"],
                "杯": ["草ダメージ", "攻撃%"],
                "冠": ["会心率", "会心ダメージ"]
            },
            "score_weight_options": COMMON_SCORE_TEMPLATES,
            "default_score_mode": "攻撃力型",
            "elixir_fixed_substats": {
                "花": ["会心率", "会心ダメージ"],
                "羽": ["会心率", "会心ダメージ"],
                "時計": ["会心率", "会心ダメージ"],
                "杯": ["会心率", "会心ダメージ"],
                "冠": ["会心率", "会心ダメージ"]
            },
            "default_target_score": 180
        }
    }
}
}