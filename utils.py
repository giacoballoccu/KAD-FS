#Implemented datasets
import os

BEAUTY = "beauty"
CD = "cd"
CELL = "cell"
CLOTH = "cloth"

#Entity lists
ENTITY_LIST = {
    BEAUTY: [],
    CD: [],
    CELL: [],
    CLOTH: [],
}

#Implemented models
KGAT = "kgat"
PGPR = "pgpr"

#Models dirs
MODEL_DIR_NAME = {
    PGPR: "./PGPR/",
    KGAT: "./KGAT/",
}

DATASET_DIR_NAME = {
    BEAUTY: "Amazon_Beauty/",
    CD: "Amazon_CDs/",
    CELL: "Amazon_Cellphones/",
    CLOTH: "Amazon_Clothing/",
}
#Particular properties that need to be handled in mappers
DATASETS_WITH_WORDS = [BEAUTY, CD, CELL, CLOTH]

MAIN_PRODUCT_INTERACTION = {
    #ML1M: (MOVIE, WATCHED),
    #LASTFM: (SONG, LISTENED),
    BEAUTY: ("product", "purchase"),
    CD: ("product", "purchase"),
    CELL: ("product", "purchase"),
    CLOTH: ("product", "purchase"),
}

RELATION_LIST = {
    BEAUTY: ["also_bought", "also_viewed", "bought_together", "belong_to", "produced_by"],
    CD: ["also_bought", "also_viewed", "bought_together", "belong_to", "produced_by"],
    CELL: ["also_bought", "also_viewed", "bought_together", "belong_to", "produced_by"],
    CLOTH: ["also_bought", "also_viewed", "bought_together", "belong_to", "produced_by"],
}

ENTITY_FROM_RELATION = {
    BEAUTY: {"also_bought": "rproduct", "also_viewed": "rproduct", "bought_together": "rproduct", "belong_to": "category", "produced_by": "brand"},
    CELL: {"also_bought": "rproduct", "also_viewed": "rproduct", "bought_together": "rproduct", "belong_to": "category", "produced_by": "brand"},
    CLOTH: {"also_bought": "rproduct", "also_viewed": "rproduct", "bought_together": "rproduct", "belong_to": "category", "produced_by": "brand"},
}

ENTITY_FROM_RELATION_FILE = {
    BEAUTY: {"also_bought_p_p": "related_product", "also_viewed_p_p": "related_product",
             "bought_together_p_p": "related_product", "category_p_c": "category", "brand_p_b": "brand"},
    CLOTH: {"also_bought_p_p": "related_product", "also_viewed_p_p": "related_product",
             "bought_together_p_p": "related_product", "category_p_c": "category", "brand_p_b": "brand"},
    CELL: {"also_bought_p_p": "related_product", "also_viewed_p_p": "related_product",
             "bought_together_p_p": "related_product", "category_p_c": "category", "brand_p_b": "brand"},
}
def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

