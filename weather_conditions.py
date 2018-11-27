# -*- coding: utf-8 -*-

class ConditionName(object):

    def name(code):

        condition_text = {
            '0': 'tornádó vazze',
            '1': 'trópusi vihar csesszemeg',
            '2': 'hurrikán bazdmeg',
            '3': 'súlyos vihar',
            '4': 'zivatarok',
            '5': 'havasesö',
            '6': 'latyak',
            '7': 'szutyok',
            '8': 'ónos esö',
            '9': 'szitálás',
            '10': 'másik ónos esö',
            '11': 'esö',
            '12': 'esö',
            '13': 'hófúvás',
            '14': 'kis havazás',
            '15': 'hófúvás',
            '16': 'winter is coming',
            '17': 'jégesö',
            '18': 'havasesö',
            '19': 'por',
            '20': 'köd',
            '21': 'hajnali köd',
            '22': 'szmogos',
            '23': 'szélvihar',
            '24': 'szél',
            '25': 'grrrr',
            '26': 'felhös',
            '27': 'felhös éjjel',
            '28': 'felhös',
            '29': 'részben felhös éj',
            '30': 'részben felhös',
            '31': 'tiszta éj',
            '32': 'napos',
            '33': 'tiszta éj',
            '34': 'tiszta',
            '35': 'jeges esö',
            '36': 'csuda meleg',
            '37': 'szórványos viharok',
            '38': 'elszórt viharok',
            '39': 'elszórt viharok 2',
            '40': 'elszórt záporok',
            '41': 'csudanagy hó',
            '42': 'elszórt havazás',
            '43': 'sok hó',
            '44': 'részlegesen felhös',
            '45': 'hóvihar',
            '46': 'hóesö',
            '47': 'szórványos zivatarok',
            '3200': 'fene se tudja'
        }

        return condition_text[code]
