from localsecrets.secretmanager import SecretManager
from localsecrets.config import DEBUG


def main():
    sm = SecretManager('/share/code/db/secrets.db', None)

    try:
        sm.add_vault('work')
    except KeyError:
        pass
    sm.set_current_vault('default')
    print(sm.item.add('accuweather','accuweather api key'))
    print(sm.item.add('not-imdb','not-imdb api key'))
    sm.save_db_file()
    sm.item.rename('not-imdb','--imdb--')
    sm['default'].rename_item('--imdb--','imdb')
    sm['default']['accuweather'].set_user_data('thiss','is used to check the weatherzz')
    sm['default']['accuweather'].set_user_data('thiss','is used to check the weather')
    sm['default']['accuweather'].rename_user_data_key('thiss','thiszzz')
    sm.item.rename_user_data_key('accuweather','thiszzz','this')
    sm.item.set_user_data('accuweather','is not','the binance api key')
    print(sm.item.get_user_data('accuweather','this'))
    print(sm['default']['accuweather'].get_user_data('is not'))
    print(sm['default']['accuweather'].list_user_data_keys())
    print(sm.item('accuweather').list_user_data_keys())
    sm.item.delete_user_data_key('accuweather','this')
    sm['default']['accuweather'].delete_user_data_key('is not')
    sm.item.purge_user_data('accuweather')
    print(sm['default']['accuweather'].list_user_data_keys())
    print(sm.item('accuweather').list_user_data_keys())
    sm.add_item('binance2','my binance api key')
    sm.add_item('accuweather2','my accuweather api key')
    sm.add_item('imdb2','my not imdb api key')
    sm.add_item('google something2','my binance api key')
    sm.item.rename('imdb2', 'not-imdb2')
    sm.item.delete('not-imdb2')
    sm.item('binance2').set_user_data('ttt','ddd')
    sm.item.delete('binance2')
    print(sm.get_secret('accuweather'))
    print(sm.get_secret('imdb'))
    sm.add_item('teste-delete','useless api key')
    sm.set_current_vault('default')
    sm.delete_vault('work')
    print(sm.list_vaults())
    print(sm.item.list_())
    print(sm.item.pprint_deleted())
    print(sm.item.list_deleted())

    uuids = sm.item.list_deleted()

    sm.add_vault('restored')
    sm.item.restore_deleted(uuids[0]['uuid'],'restored')
    print('\n\n')
    print(sm.item.search('binance', pprint=True))

    sm.save_db_file()


if __name__ == "__main__":
    main()
