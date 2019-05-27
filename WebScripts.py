import GoldScripting
import sys
sys.path.insert(0, './Database')
import database

def gold_scripts(gold):
    if gold is 'gold18k':
        if database.time_update('gold18k'):
            gold18k_data = GoldScripting.get18k()
            database.update_data('gold18k', gold18k_data)
            return gold18k_data
        else:
            return database.read_data('gold18k')
    elif gold is 'gold24k':
        if database.time_update('gold24k'):
            gold24k_data = GoldScripting.get24k()
            database.update_data('gold24k', gold24k_data)
            return gold24k_data
        else:
            return database.read_data('gold24k')
    elif gold is 'gold_ons':
        if database.time_update('gold_ons'):
            gold_ons_data = GoldScripting.get_ons()
            database.update_data('gold_ons', gold_ons_data)
            return gold_ons_data
        else:
            return database.read_data('gold_ons')
