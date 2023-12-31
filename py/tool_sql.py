# from helper_suql import ContextParser, InferenceParser, WholisticParser
# from domain_knowledge import GiftDataset2, TvDataset, AcDataset

# from model_base import OpenaiBase

# import sqlite3
import mysql.connector


class DatabaseInstance():
    
    # def __init__(self, 
    #              database_name="tutorial.db"):
    #     self.db_connection = sqlite3.connect(database_name)
    #     self.db_cursor = self.db_connection.cursor()

    # Google Cloud SQL database

    def __init__(self, 
                 db_host="10.11.64.4",
                 db_user="jean-cs224v-db",
                 db_password="Password!1",
                 db_name="224v-project"):
        self.db_connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        self.db_cursor = self.db_connection.cursor()

    def get_db_connection(self):
        return self.db_connection

    def get_db_cursor(self):
        return self.db_cursor


class GiftOracle():

    def __init__(self, n,                 
                 completion_llm):
        domain_name="CLIQ"
        domain_datasets=[GiftDataset2()]
        picked_columns=['id', 'price', 
                        'brand', 'colors',
                        'category', 'store', 'gender',
                        'title', 'description']
        primary_key='id'
        price_column = 'price'
        summarize_columns=['title', 'description']
        self.db_instance = DatabaseInstance()
        self.context_parser = ContextParser(n, domain_name, domain_datasets, 
                picked_columns, primary_key, price_column, summarize_columns,
                self.db_instance, completion_llm, is_verbose=False)
        column_annotation = { 
            "for_people": {
                "style_setters": ["dinner_sets", "candle_holders", "candles"], 
                "wellness_lovers": ["dryfruits", "tea_sets"], 
                "fitness_buffs": ["speaker_mediaplayer"], 
                "gamers": ["gaming", "headphones_earphones"], 
                "home_chefs": ["dinner_sets"], 
                "gear_heads": [], 
                "DIYers": [],
                "adventure_seekers": [], 
                "trending_gifts": []
                },
            "shop_gifts": {
                "for_her": ["wallets-women", "watch-women", "fragrances-women", "handbags-women", "backpacks-women"], 
                "for_him": ["wallets-men", "watch-men", "fragrances-men", "backpacks-men"], 
                "for_teens": [], 
                "for_kids": ["watch-kids", "watch-kids"],
                "babies_and_toddlers": [], 
                "for_pets": []
            },
            "by_category": {
                "toys": [], 
                "electronics": ["headphones_earphones", "instant_camera", "mobiles", "speaker_mediaplayer", "tab_ereader"], 
                "fashion": [], 
                "home_and_kitchen": ["bedsheets", "candle_holders", "dinner_sets", "tea_sets", "home_fragrances"],
                "sports_and_outdoors": [], 
                "beauty": []
                },
            "holiday_shopping": {
                "most_loved_gifts": ["chocolates", "sweets"], 
                "decor": ["candle_holders", "silver_artifacts"],
                "gifts_for_all": ["drinking_glass"], 
                "toys": [], 
                "stocking_stuffers": ["chocolates", "sweets"],
                "unique_gifts": ["silver_bullion"], 
                "hosting_essentials": [], 
                "white_elephant": [],
                "same_day_delivery": []
            }
        }        
        self.inference_parser = InferenceParser(n, domain_name, domain_datasets, 
                picked_columns, primary_key, price_column, summarize_columns, column_annotation, 
                self.db_instance, completion_llm, is_verbose=False)
        self.wholistic_parser = WholisticParser(self.context_parser, self.inference_parser)

    def get_context_parser(self):
        return self.context_parser

    def get_inference_parser(self):
        return self.inference_parser

    def get_wholistic_parser(self):
        return self.wholistic_parser

    def get_db_cursor(self):
        return self.db_instance.get_db_cursor()


class ProductRetriever():

    def __init__(self):
        pass


class ProductReader():

    def __init__(self):
        pass    