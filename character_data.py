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
                "default_target_score": 180
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

    "胡桃": {
    "element": "炎",
    "weapon": "長柄武器",
    "builds": {
        "アタッカー": {
            "fixed_mainstats": {
                "花": "HP",
                "羽": "攻撃力"
            },
            "mainstat_options": {
                "時計": ["HP%", "元素熟知"],
                "杯": ["炎ダメージ", "HP%"],
                "冠": ["会心率", "会心ダメージ"]
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
}