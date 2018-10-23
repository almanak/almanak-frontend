# -*- coding: UTF-8 -*-

import os
import urllib.request, urllib.parse, urllib.error
import json
from copy import deepcopy

import requests

import serviceInterface

OAWS_API_KEY = os.environ.get('OAWS_API_KEY')

FACETS = {
    'content_types': {
        'label': 'Materialetype',
        'multiple': True,
        'hierarchical': True,
        'content': [
            {
                "id": "99",
                "label": "Andet materiale"
            },
            {
                "children": [
                  {
                    "id": "66",
                    "icon": "far fa-image",
                    "label": "Afbildning af arkitektur og bygning"
                  },
                  {
                    "id": "65",
                    "icon": "far fa-image",
                    "label": "Afbildning af kunst"
                  },
                  {
                    "id": "73",
                    "icon": "far fa-image",
                    "label": "Arkitekturtegning"
                  },
                  {
                    "id": "64",
                    "icon": "far fa-image",
                    "label": "By- og gadebilleder"
                  },
                  {
                    "id": "70",
                    "icon": "far fa-image",
                    "label": "Collage"
                  },
                  {
                    "id": "71",
                    "icon": "far fa-image",
                    "label": "Illustrationer"
                  },
                  {
                    "id": "100",
                    "icon": "far fa-image",
                    "label": "Landskabs- og naturbilleder"
                  },
                  {
                    "id": "62",
                    "icon": "far fa-image",
                    "label": "Luftfoto"
                  },
                  {
                    "id": "68",
                    "icon": "far fa-image",
                    "label": "Maleri"
                  },
                  {
                    "id": "67",
                    "icon": "far fa-image",
                    "label": "Plakat"
                  },
                  {
                    "id": "69",
                    "icon": "far fa-image",
                    "label": "Planche"
                  },
                  {
                    "id": "63",
                    "icon": "far fa-image",
                    "label": "Portræt"
                  },
                  {
                    "id": "74",
                    "icon": "far fa-image",
                    "label": "Postkort"
                  },
                  {
                    "id": "72",
                    "icon": "far fa-image",
                    "label": "Tekniske tegninger"
                  }
                ],
                "id": "61",
                "icon": "far fa-image",
                "label": "Billeder"
              },
              {
                "children": [
                  {
                    "id": "98",
                    "icon": "fas fa-laptop",
                    "label": "Hjemmesider"
                  },
                  {
                    "id": "96",
                    "icon": "fas fa-laptop",
                    "label": "Software"
                  },
                  {
                    "id": "97",
                    "icon": "fas fa-laptop",
                    "label": "Spil"
                  }
                ],
                "id": "95",
                "icon": "fas fa-laptop",
                "label": "Elektronisk materiale"
              },
              {
                "children": [
                  {
                    "description": "Skøder, pantebreve, forpagtningskontrakter, m.m.",
                    "id": "13",
                    "icon": "fas fa-gavel",
                    "label": "Ejendomspapirer"
                  },
                  {
                    "id": "12",
                    "icon": "fas fa-gavel",
                    "label": "Kontrakter"
                  },
                  {
                    "id": "16",
                    "icon": "fas fa-gavel",
                    "label": "Love og cirkulærer"
                  },
                  {
                    "id": "15",
                    "icon": "fas fa-gavel",
                    "label": "Regulativer"
                  },
                  {
                    "id": "11",
                    "icon": "fas fa-gavel",
                    "label": "Retningslinier"
                  },
                  {
                    "id": "17",
                    "icon": "fas fa-gavel",
                    "label": "Standarder og specifikationer"
                  },
                  {
                    "id": "14",
                    "icon": "fas fa-gavel",
                    "label": "Vedtægter"
                  }
                ],
                "id": "10",
                "icon": "fas fa-gavel",
                "label": "Forskrifter og vedtægter"
              },
              {
                "children": [
                  {
                    "id": "5",
                    "icon": "far folder-open",
                    "label": "Borgersager"
                  },
                  {
                    "id": "2",
                    "icon": "far folder-open",
                    "label": "Bygge- og ejendomssager"
                  },
                  {
                    "id": "8",
                    "icon": "far folder-open",
                    "label": "By- og lokalplaner"
                  },
                  {
                    "id": "7",
                    "icon": "far folder-open",
                    "label": "Byråds- og udvalgssager"
                  },
                  {
                    "id": "4",
                    "icon": "far folder-open",
                    "label": "Emnesager"
                  },
                  {
                    "id": "9",
                    "icon": "far folder-open",
                    "label": "Kommunalplaner"
                  },
                  {
                    "id": "6",
                    "icon": "far folder-open",
                    "label": "Personalesager"
                  },
                  {
                    "id": "3",
                    "icon": "far folder-open",
                    "label": "Vej og område, kulturmiljøsager"
                  }
                ],
                "id": "1",
                "icon": "far folder-open",
                "label": "Kommunale sager og planer"
              },
              {
                "children": [
                  {
                    "id": "80",
                    "icon": "far fa-map",
                    "label": "Diagram"
                  },
                  {
                    "id": "76",
                    "icon": "far fa-map",
                    "label": "Matrikelkort"
                  },
                  {
                    "id": "79",
                    "icon": "far fa-map",
                    "label": "Tekniske kort"
                  },
                  {
                    "id": "77",
                    "icon": "far fa-map",
                    "label": "Topografiske kort"
                  },
                  {
                    "id": "78",
                    "icon": "far fa-map",
                    "label": "Økonomiske kort"
                  }
                ],
                "id": "75",
                "icon": "far fa-map",
                "label": "Kortmateriale"
              },
              {
                "description": "upubliceret",
                "children": [
                  {
                    "description": "upubliceret",
                    "id": "51",
                    "icon": "far file-alt",
                    "label": "Afhandlinger og disputatser"
                  },
                  {
                    "description": "upubliceret",
                    "id": "53",
                    "icon": "far file-alt",
                    "label": "Eksamensopgaver"
                  },
                  {
                    "description": "upubliceret",
                    "id": "50",
                    "icon": "far file-alt",
                    "label": "Erindringer og dagbøger"
                  },
                  {
                    "description": "upubliceret",
                    "id": "52",
                    "icon": "far file-alt",
                    "label": "Forelæsningspapirer og -noter"
                  },
                  {
                    "description": "upubliceret",
                    "id": "56",
                    "icon": "far file-alt",
                    "label": "Håndbøger og manualer"
                  },
                  {
                    "description": "upubliceret, email, chat, breve, interviews",
                    "id": "60",
                    "icon": "far file-alt",
                    "label": "Korrespondance"
                  },
                  {
                    "description": "upubliceret, skudsmålsbøger, eksamenspapirer, anbefalinger, attester, m.m.",
                    "id": "58",
                    "icon": "far file-alt",
                    "label": "Personlige papirer"
                  },
                  {
                    "description": "upubliceret, arkivalske registranter",
                    "id": "59",
                    "icon": "far file-alt",
                    "label": "Registranter"
                  },
                  {
                    "description": "upubliceret, festtaler, oratoriske taler, politiske taler m.m.",
                    "id": "54",
                    "icon": "far file-alt",
                    "label": "Taler"
                  },
                  {
                    "description": "upubliceret",
                    "id": "57",
                    "icon": "far file-alt",
                    "label": "Tweets, online posts, blogs"
                  },
                  {
                    "description": "upubliceret",
                    "id": "55",
                    "icon": "far file-alt",
                    "label": "Udklip og småtryk"
                  }
                ],
                "id": "49",
                "icon": "far file-alt",
                "label": "Manuskripter"
              },
              {
                "description": "tv, radio og internet",
                "children": [
                  {
                    "description": "tv, radio og internet",
                    "id": "93",
                    "icon": "fas fa-film",
                    "label": "Animation"
                  },
                  {
                    "description": "tv, radio og internet",
                    "id": "89",
                    "icon": "fas fa-film",
                    "label": "Dokumentarer"
                  },
                  {
                    "description": "tv, radio og internet",
                    "id": "90",
                    "icon": "fas fa-film",
                    "label": "Eksperimental videokunst"
                  },
                  {
                    "description": "tv, radio og internet",
                    "id": "92",
                    "icon": "fas fa-film",
                    "label": "Fiktion og kortfilm"
                  },
                  {
                    "description": "tv, radio og internet",
                    "id": "91",
                    "icon": "fas fa-film",
                    "label": "Magasin- og nyhedsprogrammer"
                  },
                  {
                    "description": "tv, radio og internet",
                    "id": "94",
                    "icon": "fas fa-film",
                    "label": "Oplæsninger"
                  },
                  {
                    "description": "tv, radio og internet",
                    "id": "88",
                    "icon": "fas fa-film",
                    "label": "Reportager"
                  }
                ],
                "id": "87",
                "icon": "fas fa-film",
                "label": "Medieproduktioner"
              },
              {
                "children": [
                  {
                    "id": "86",
                    "label": "Ikke-musikalsk lyd"
                  },
                  {
                    "id": "85",
                    "label": "Live-opførelser"
                  },
                  {
                    "id": "82",
                    "label": "Musikudgivelser"
                  },
                  {
                    "id": "83",
                    "label": "Noder"
                  },
                  {
                    "id": "84",
                    "label": "Sange og salmer"
                  }
                ],
                "id": "81",
                "label": "Musik og lydoptagelser"
              },
              {
                "children": [
                  {
                    "description": "inkl. anmeldelser, nekrologer, opiniods, m.m.",
                    "id": "41",
                    "icon": "fas fa-book",
                    "label": "Artikler og essays"
                  },
                  {
                    "description": "inkl. diskografi, filmografi og andre værkfortegnelse",
                    "id": "40",
                    "icon": "fas fa-book",
                    "label": "Bibliografier"
                  },
                  {
                    "id": "44",
                    "icon": "fas fa-book",
                    "label": "Detailkataloger, reklamer, propaganda"
                  },
                  {
                    "id": "37",
                    "icon": "fas fa-book",
                    "label": "Faglitteratur"
                  },
                  {
                    "description": "Vejvisere, telefonbøger, m.m.",
                    "id": "46",
                    "icon": "fas fa-book",
                    "label": "Fortegnelser"
                  },
                  {
                    "id": "45",
                    "icon": "fas fa-book",
                    "label": "Kataloger og programmer for diverse"
                  },
                  {
                    "id": "47",
                    "icon": "fas fa-book",
                    "label": "Nyhedsbreve og medlemsblade"
                  },
                  {
                    "id": "43",
                    "icon": "fas fa-book",
                    "label": "Pjecer, pamfletter"
                  },
                  {
                    "id": "48",
                    "icon": "fas fa-book",
                    "label": "Rapporter"
                  },
                  {
                    "description": "encyklopædier, ordbøger, m.m.",
                    "id": "39",
                    "icon": "fas fa-book",
                    "label": "Reference- og opslagsværker"
                  },
                  {
                    "description": "inkl. autobiografier",
                    "id": "38",
                    "icon": "fas fa-book",
                    "label": "Skønlitteratur, dramatik og poesi"
                  },
                  {
                    "description": "magasiner, årspublikationer, periodica, m.m.",
                    "id": "42",
                    "icon": "fas fa-book",
                    "label": "Tidsskrifter og aviser"
                  }
                ],
                "id": "36",
                "icon": "fas fa-book",
                "label": "Publikationer"
              },
              {
                "children": [
                  {
                    "id": "27",
                    "icon": "fab fa-leanpub",
                    "label": "Andre registre og protokoller"
                  },
                  {
                    "id": "22",
                    "icon": "fab fa-leanpub",
                    "label": "Brandtaksationsprotokoller"
                  },
                  {
                    "description": "Lister, medlemsfortegnelser, adressefortegnelser, navnelister, m.m.",
                    "id": "28",
                    "icon": "fab fa-leanpub",
                    "label": "Diverse fortegnelser"
                  },
                  {
                    "id": "20",
                    "icon": "fab fa-leanpub",
                    "label": "Dødsattester og -journaler"
                  },
                  {
                    "id": "24",
                    "icon": "fab fa-leanpub",
                    "label": "Folketællinger"
                  },
                  {
                    "id": "25",
                    "icon": "fab fa-leanpub",
                    "label": "Kirkebøger"
                  },
                  {
                    "id": "19",
                    "icon": "fab fa-leanpub",
                    "label": "Mødereferater og forhandlingsprotokoller"
                  },
                  {
                    "id": "23",
                    "icon": "fab fa-leanpub",
                    "label": "Realregistre"
                  },
                  {
                    "id": "21",
                    "icon": "fab fa-leanpub",
                    "label": "Skattemandtalslister"
                  },
                  {
                    "id": "26",
                    "icon": "fab fa-leanpub",
                    "label": "Skifteprotokoller"
                  }
                ],
                "id": "18",
                "icon": "fab fa-leanpub",
                "label": "Registre og protokoller"
              },
              {
                "children": [
                  {
                    "id": "34",
                    "icon": "far chart-bar",
                    "label": "Database"
                  },
                  {
                    "id": "31",
                    "icon": "far chart-bar",
                    "label": "Regnskaber og budgetmateriale"
                  },
                  {
                    "id": "30",
                    "icon": "far chart-bar",
                    "label": "Spørgeskemaundersøgelser"
                  },
                  {
                    "id": "32",
                    "icon": "far chart-bar",
                    "label": "Statistisk materiale"
                  },
                  {
                    "id": "33",
                    "icon": "far chart-bar",
                    "label": "Statistisk undersøgelse"
                  },
                  {
                    "id": "35",
                    "icon": "far chart-bar",
                    "label": "Tabelværk"
                  }
                ],
                "id": "29",
                "icon": "far chart-bar",
                "label": "Statistisk og økonomisk materiale"
              }
        ]
    },
    'subjects': {
        'label': 'Emnekategori',
        'multiple': True,
        'hierarchical': True,
        'content': [
            {
                'id': '17',
                'label': 'Erhverv',
                'children': [
                    {
                        'id': '53',
                        'label': 'Banker og Sparekasser',
                    },
                    {
                        'id': '14',
                        'label': 'Detailhandel og service',
                    },
                    {
                        'id': '13',
                        'label': 'Fagforeninger',
                    },
                    {
                        'id': '66',
                        'label': 'Fiskeri og jagt',
                    },
                    {
                        'id': '15',
                        'label': 'Håndværk og industri',
                    },
                    {
                        'id': '57',
                        'label': 'Kooperation',
                    },
                    {
                        'id': '54',
                        'label': 'Kost og logi',
                    },
                    {
                        'id': '16',
                        'label': 'Land- og skovbrug',
                    },
                    {
                        'id': '55',
                        'label': 'Turistvæsen',
                    }
                ]
            },
            {
                'id': '29',
                'label': 'Historiske perioder og temaer',
                'children': [
                    {
                        'id': '4',
                        'label': 'Myter og sagn',
                    },
                    {
                        'id': '28',
                        'label': 'Oldtid',
                    },
                    {
                        'id': '51',
                        'label': 'Vikingetiden',
                    },
                    {
                        'id': '30',
                        'label': 'Indtil 1536',
                    },
                    {
                        'id': '72',
                        'label': '1536-1660',
                    },
                    {
                        'id': '69',
                        'label': '1660-1814',
                    },
                    {
                        'id': '68',
                        'label': 'Det 19. århundrede',
                    },
                    {
                        'id': '31',
                        'label': 'Det 20. århundrede',
                    },
                    {
                        'id': '70',
                        'label': 'Besættelsen',
                    },
                    {
                        'id': '7',
                        'label': 'Det 21. århundrede',
                    }
                ]
            },
            {
                'id': '37',
                'label': 'Kultur og fritid',
                'children': [
                    {
                        'id': '34',
                        'label': 'Arkitektur',
                    },
                    {
                        'id': '33',
                        'label': 'Arrangementer og festtraditioner',
                    },
                    {
                        'id': '56',
                        'label': 'Folkekultur og dagligdagsliv',
                    },
                    {
                        'id': '35',
                        'label': 'Forlystelser, spil og idræt',
                    },
                    {
                        'id': '76',
                        'label': 'Kulturinstitutioner',
                    },
                    {
                        'id': '74',
                        'label': 'Kunst og litteratur',
                    },
                    {
                        'id': '73',
                        'label': 'Mad og drikke',
                    },
                    {
                        'id': '36',
                        'label': 'Musik',
                    },
                    {
                        'id': '75',
                        'label': 'Skulpturer og offentlig kunst',
                    },
                    {
                        'id': '1',
                        'label': 'Teater, film, radio og tv',
                    }
                ]
            },
            {
                'id': '62',
                'label': 'Natur',
                'children': [
                    {
                        'id': '59',
                        'label': 'Kilder',
                    },
                    {
                        'id': '58',
                        'label': 'Skove',
                    },
                    {
                        'id': '61',
                        'label': 'Strand og bugt',
                    },
                    {
                        'id': '60',
                        'label': 'Søer',
                    },
                    {
                        'id': '12',
                        'label': 'Åer og bække',
                    }
                ]
            },
            {
                'id': '42',
                'label': 'Personer',
                'children': [
                    {
                        'id': '39',
                        'label': 'Arkitekter og bygmestre',
                    },
                    {
                        'id': '38',
                        'label': 'Embedsmænd',
                    },
                    {
                        'id': '41',
                        'label': 'Erhvervsfolk',
                    },
                    {
                        'id': '21',
                        'label': 'Gejstlige',
                    },
                    {
                        'id': '40',
                        'label': 'Historiske personer',
                    },
                    {
                        'id': '22',
                        'label': 'Journalister og pressefotografer',
                    },
                    {
                        'id': '19',
                        'label': 'Kulturpersoner',
                    },
                    {
                        'id': '18',
                        'label': 'Politikere',
                    },
                    {
                        'id': '20',
                        'label': 'Undervisere og forskere',
                    }
                ]
            },
            {
                'id': '3',
                'label': 'Samfund',
                'children': [
                    {
                        'id': '71',
                        'label': 'Beskæftigelse og arbejdsløshed',
                    },
                    {
                        'id': '5',
                        'label': 'Bolig, byggeri og byplanlægning',
                    },
                    {
                        'id': '47',
                        'label': 'Foreninger',
                    },
                    {
                        'id': '44',
                        'label': 'Kommunal forvaltning',
                    },
                    {
                        'id': '43',
                        'label': 'Kommunikation og medier',
                    },
                    {
                        'id': '6',
                        'label': 'Lovgivning og jura',
                    },
                    {
                        'id': '45',
                        'label': 'Militær',
                    },
                    {
                        'id': '27',
                        'label': 'Penge og økonomi',
                    },
                    {
                        'id': '24',
                        'label': 'Politi, brand og redning',
                    },
                    {
                        'id': '23',
                        'label': 'Politik',
                    },
                    {
                        'id': '46',
                        'label': 'Religion og kirke',
                    },
                    {
                        'id': '25',
                        'label': 'Socialpolitik og velfærd',
                    },
                    {
                        'id': '67',
                        'label': 'Sundhedsvæsen',
                    },
                    {
                        'id': '64',
                        'label': 'Trafik og transport',
                    },
                    {
                        'id': '53',
                        'label': 'Ud- og indvandring',
                    },
                    {
                        'id': '26',
                        'label': 'Undervisning og uddannelse',
                    },
                    {
                        'id': '65',
                        'label': 'Videnskab og forskning',
                    }
                ]
            },
            {
                'id': '9',
                'label': 'Steder',
                'children': [
                    {
                        'id': '8',
                        'label': 'Byer og bydele',
                    },
                    {
                        'id': '10',
                        'label': 'Ejendomme og bygningsværker',
                    },
                    {
                        'id': '52',
                        'label': 'Gader og veje',
                    },
                    {
                        'id': '49',
                        'label': 'Kirker',
                    },
                    {
                        'id': '48',
                        'label': 'Parker og anlæg',
                    },
                    {
                        'id': '11',
                        'label': 'Slotte og herregårde',
                    },
                    {
                        'id': '50',
                        'label': 'Sogne',
                    },
                    {
                        'id': '32',
                        'label': 'Torve og pladser',
                    }
                ]
            },
            {
                'id': '2',
                'label': 'Andet',
            }
        ]
    },
    'availability': {
        'label': 'Tilgængelighed',
        'multiple': False,
        'hierarchical': False,
        'content': [
            {
                'id': '2',
                'label': 'På magasin',
            },
            {
                'id': '3',
                'label': 'Kan ses på læsesalen',
            },
            {
                'id': '4',
                'label': 'Kan ses online',
            }
        ]
    },
    'usability': {
        'label': 'Brug af materialer',
        'multiple': False,
        'hierarchical': False,
        'content': [
            {
                'id': '1',
                'label': 'I offentlig eje',
            },
            {
                'id': '2',
                'label': 'CC Navngivelse',
            },
            {
                'id': '3',
                'label': 'CC Navngivelse-IkkeKommerciel',
            },
            {
                'id': '4',
                'label': 'Alle rettigheder forbeholdes',
            }
        ]
    }
}

FILTERS = {
    'creators': {
        'label': 'Ophavsretsholder',
        'repeatable': True,
        'type': 'object',
    },
    'locations': {
        'label': 'Stedsangivelse',
        'repeatable': True,
        'type': 'object',
    },
    'events': {
        'label': 'Forestilling',
        'repeatable': True,
        'type': 'object',
    },
    'people': {
        'label': 'Person',
        'repeatable': True,
        'type': 'object',
    },
    'organisations': {
        'label': 'Organisation',
        'repeatable': True,
        'type': 'object',
    },
    'collection': {
        'label': 'Samling',
        'repeatable': False,
        'type': 'object',
    },
    'date_from': {
        'label': 'Startdato',
        'repeatable': False,
        'type': 'string',
    },
    'date_to': {
        'label': 'Slutdato',
        'repeatable': False,
        'type': 'string',
    },
    'subjects': {
        'label': 'Emnekategori',
        'repeatable': True,
        'type': 'object',
    },
    'series': {
        'label': 'Serie',
        'repeatable': False,
        'type': 'string',
    },
    'admin_tags': {
        'label': 'Tag',
        'repeatable': True,
        'type': 'string',
    },
    'collection_tags': {
        'label': 'Samlingstags',
        'repeatable': True,
        'type': 'string',
    },
    'content_types': {
        'label': 'Materialetype',
        'repeatable': True,
        'type': 'object',
    },
    'collectors': {
        'label': 'Arkivskaber',
        'repeatable': True,
        'type': 'object',
    },
    'curators': {
        'label': 'Kurator',
        'repeatable': True,
        'type': 'object',
    },
    'availability': {
        'label': 'Tilgængelighed',
        'repeatable': False,
        'type': 'object',
    },
    'sort': {
        'label': 'Sortering',
        'repeatable': False,
        'type': 'string',
    },
    'size': {
        'label': 'Antal visninger',
        'repeatable': False,
        'type': 'integer',
    },
    'start': {
        'label': 'Start',
        'repeatable': False,
        'type': 'integer',
    },
    'usability': {
        'label': 'Hvad må jeg bruge?',
        'repeatable': False,
        'type': 'object'
    },
    'registration_id': {
        'label': 'RegistreringsID',
        'repeatable': False,
        'type': 'integer'
    }
}


class Client():

    # def __init__(self, config):
    def __init__(self):
        self.facets = FACETS
        self.filters = FILTERS
        self.service = serviceInterface.Service(OAWS_API_KEY)
        self.service_url = 'https://openaws.appspot.com'
        self.resources = {
            'records': 'records_v3',
            'people': 'entities',
            'locations': 'entities',
            'organisations': 'entities',
            'events': 'entities',
            'creators': 'entities',
            'collectors': 'entities',
            'objects': 'objects',
            'collections': 'collections'
        }

    # def list_collections(self):
    #     response = self._get_request("https://openaws.appspot.com/collections")
    #     if response.get('status_code') == 0:
    #         return response.result
    #     else:
    #         return {"error": response.get('status_code'),
    #                 "msg": response.get('status_msg')}

    def list_facets_v2(self):
        def encode(key, val):
            utf8_param = [(key, str(val).encode('utf-8'))]
            return urllib.parse.urlencode(utf8_param)

        facets = self.service.list_facets()
        result = {}

        for facet in facets:
            out = {}
            for b in facets[facet].get('buckets'):
                b['add_link'] = encode(facet, b.get('value'))
                out[b.get('value')] = b
            result[facet] = out
        return {'total_facets': self.facets, 'active_facets': result}

    def list_resources(self, query_params=None):

        def _generate_views(params, view):
            output = []
            views = [
                {
                    'label': 'Listevisning',
                    'value': 'list',
                    'icon': 'fas fa-list'  # 'view_list'
                },
                {
                    'label': 'Galleri-visning',
                    'value': 'gallery',
                    'icon': 'fas fa-th'  # 'view_module'
                }
            ]

            if params:
                stripped_params = [(t[0], t[1]) for t in params if t[0] != 'view']
            else:
                stripped_params = []

            for option in views:
                current = {}
                current['label'] = option.get('label')
                current['icon'] = option.get('icon')
                if option.get('value') == view:
                    current['selected'] = True
                else:
                    current['link'] = _urlencode(stripped_params + [('view', option.get('value'))])
                output.append(current)
            return output

        def _generate_sorts(params, sort, direction):
            sorts = [
                {
                    'label': 'Ældste dato først',
                    'sort': 'date_from',
                    'icon': 'fas fa-long-arrow-alt-up',  # 'arrow_upward'
                    'direction': 'asc'
                },
                {
                    'label': 'Nyeste dato først',
                    'sort': 'date_to',
                    'icon': 'fas fa-long-arrow-alt-down',  # 'arrow_downward'
                    'direction': 'desc'
                },
                {
                    'label': 'Relevans',
                    'sort': '_score',
                    'direction': 'desc'
                }
            ]
            output = []

            if params:
                stripped_params = [(t[0], t[1]) for t in params if t[0] not in ['sort', 'direction', 'start']]
            else:
                stripped_params = []

            for option in sorts:
                current = {}
                current['icon'] = option.get('icon')
                current['label'] = option.get('label')
                if option.get('sort') == sort and option.get('direction') == direction:
                    current['selected'] = True
                else:
                    current['link'] = _urlencode(stripped_params + [('sort', option.get('sort')), ('direction', option.get('direction'))])
                output.append(current)
            return output

        def _generate_sizes(params, size):
            sizes = [20, 50, 100]
            output = []

            if params:
                stripped_params = [(t[0], t[1]) for t in params if t[0] != 'size']
            else:
                stripped_params = []

            for option in sizes:
                current = {}
                current['label'] = option
                if option == size:
                    current['selected'] = True
                else:
                    current['link'] = _urlencode(stripped_params + [('size', option)])
                output.append(current)
            return output

        def _generate_filters_v2(filters, params):
            # Takes filters-array of filters and adds view- and remove-links
            for f in filters:
                # If resolve_params has a display_label equal to "ID Missing"
                if f.get('error'):
                    continue

                key = f.get('key')
                value = f.get('value')
                negated = f.get('negated')

                # View_link
                # 'label' indicates an id-based filter, which has
                # an id and has been resolved
                if f.get('label'):
                    if key == 'collection':
                        f['view_link'] = "/".join(['collections', value])
                    else:
                        f['view_link'] = "/".join([key, value])

                # Remove_link
                # If positive collection, also remove series
                # negative collection-params works like normal param
                if key == 'collection' and not negated:
                    new_params = [(k, v) for k, v in params if k not in ['collection', 'series', 'start']]
                    f['remove_link'] = _urlencode(new_params)
                else:
                    new_params = [(k, v) for k, v in params if k not in ['start']]
                    original_key = '-' + key if negated else key
                    f['remove_link'] = _urlencode(new_params,
                                                  remove=(original_key, value))

                # Inverse_link
                # If negated, replace with positive, vice versa
                # exception: if positive collection, remove series-param, as
                # it follows the positive collection
                if negated:
                    new_params = [(k, v) for k, v in params if k not in ['start']]
                    f['invert_link'] = _urlencode(new_params,
                                                  insert=(key, value),
                                                  remove=('-' + key, value))
                else:
                    if key == 'collection':
                        new_params = [(k, v) for k, v in params if k not in ['collection', 'series']]
                        f['invert_link'] = _urlencode(new_params,
                                                      insert=('-' + key, value))
                    else:
                        new_params = [(k, v) for k, v in params if k not in ['start']]
                        f['invert_link'] = _urlencode(new_params,
                                                      insert=('-' + key, value),
                                                      remove=(key, value))

                if key in ['people', 'organisations']:
                    response = self._get_request("https://openaws.appspot.com/entities/" + value)
                    if response.get('status_code') == 0:
                        entity = response.get('result')

                        if entity.get('is_creative_creator'):
                            f['creator_link'] = "creators=" + value
                        if entity.get('is_creator'):
                            f['creator_link'] = "collectors=" + value

            return filters

        def _generate_facets_v2(facets, params=None):

            def _generate_facet(name, active_facets, params):

                def _recursive(name, total_facets, active_facets, params):

                    for d in total_facets:
                        _id = d.get('id')

                        if _id in list(active_facets.keys()):
                            d['count'] = active_facets.get(_id)

                            current = (name, _id)
                            if params and (current in params):
                                rm_params = [x for x in params if x != current]
                                d['remove_link'] = _urlencode_v2(rm_params)
                                # i['remove_link'] = _urlencode(params,
                                #                               remove=current)
                            elif params:
                                add_params = params + [current]
                                d['add_link'] = _urlencode_v2(add_params)
                                # i['add_link'] = _urlencode(params,
                                #                            insert=current)
                            else:
                                d['add_link'] = _urlencode_v2([current])

                            if d.get('children'):
                                _recursive(name, d.get('children'),
                                           active_facets, params)

                    return total_facets

                facet_label = self.facets[name].get('label')
                total_facets = deepcopy(self.facets[name].get('content'))
                linked_tree = _recursive(name, total_facets, active_facets, params)

                return {"label": facet_label, 'content': linked_tree}

            output = {}
            for facet_name in facets:
                # extract id and count from aws-output
                buckets = facets[facet_name].get('buckets')
                active_facets = {b.get('value'): b.get('count') for b in buckets}
                # generate links recursively
                output[facet_name] = _generate_facet(facet_name,
                                                     active_facets,
                                                     params)

            return output

        def _generate_facets_v3(facets, params=None):
            result = {}
            for facet in facets:
                out = {}
                for b in facets[facet].get('buckets'):
                    active = (facet, b.get('value'))
                    if params and (active in params):
                        rm_params = [x for x in params if x != active]
                        b['remove_link'] = _urlencode_v2(rm_params)
                    elif params:
                        b['add_link'] = _urlencode_v2(params + [active])
                    else:
                        b['add_link'] = _urlencode_v2([active])
                    out[b.get('value')] = b
                result[facet] = out
            return result

        def _urlencode_v2(params):
            # params must be a list of tuple(s)
            if not params:
                return "root"
            else:
                utf8_params = [(t[0], str(t[1]).encode('utf-8')) for t in params]
                return urllib.parse.urlencode(utf8_params)

        def _urlencode(params=None, remove=None, insert=None):
            # Like original _urlencode, but added utf8-encoding before
            # returning urlencoded params
            temp_params = deepcopy(params) if params else []
            if remove and not insert:
                if remove in temp_params:
                    temp_params.remove(remove)
            elif remove and insert:
                if remove in temp_params:
                    loc = temp_params.index(remove)
                    temp_params[loc] = insert
                else:
                    temp_params.append(insert)
            elif insert:
                    temp_params.append(insert)

            utf8_params = [(t[0], str(t[1]).encode('utf-8')) for t in temp_params]
            return urllib.parse.urlencode(utf8_params)

        # If requesting af list of collections
        if query_params.get('resource', '') == 'collections':
            response = self._get_request("https://openaws.appspot.com/collections")
            if response.get('status_code') == 0:
                return response.result
            else:
                return {"error": response.get('status_code'),
                        "msg": response.get('status_msg')}

        # If SAM-request (view=ids) or fmt=json, return without adding further keys
        # if query_params.get('view', '') == 'ids':
        if 'ids' in query_params.getlist('view'):
            return self.service.list_resources_v2(query_params)

        # Else return fullblown response
        resp = self.service.list_resources_v2(query_params)

        # Convert Immutable MultiDict to mutable list of tuples
        # http://werkzeug.pocoo.org/docs/0.13/datastructures/#werkzeug.datastructures.MultiDict
        # processed_params = [tup for tup in query_params.iteritems(multi=True)]
        processed_params = list(query_params.items())

        # Keys used for generating searchviews and facets
        resp['params'] = processed_params

        resp['collection_search'] = query_params.get('collection', False)

        resp['filters'] = _generate_filters_v2(resp['server_filters'],
                                               processed_params)
        resp['active_facets'] = _generate_facets_v3(resp['server_facets'],
                                                    processed_params)

        # 'non_query_params' is used to generate a remove_link for the q-param
        # which is not processed in _generate_filter()
        query = query_params.get('q')
        if query:
            other_params = [i for i in processed_params if i != ('q', query)]
            resp['non_query_params'] = _urlencode_v2(other_params)

        # Just testing - remove?
        resp['total_facets'] = self.facets

        # Client-params dependent on valid response
        if resp.get('status_code') == 0:

            total = resp['total']
            start = resp['start']
            size = resp['size']

            # Append to service-response
            resp['size_list'] = _generate_sizes(processed_params, size)
            resp['sort_list'] = _generate_sorts(processed_params,
                                                resp['sort'],
                                                resp['direction'])
            resp['view_list'] = _generate_views(processed_params,
                                                query_params.get('view',
                                                                 'list'))
            resp['view'] = query_params.get('view', 'list')

            if resp.get('result'):
                rm_tup = ('start', str(start))
                if start > 0:
                    resp['first'] = _urlencode(processed_params,
                                               remove=rm_tup)
                    resp['previous'] = _urlencode(processed_params,
                                                  remove=rm_tup,
                                                  insert=('start',
                                                          start - size))

                if total <= 10000 and (start + size < total):
                    last_start = total / size * size
                    resp['last'] = _urlencode(processed_params,
                                              remove=rm_tup,
                                              insert=('start', last_start))

                if (start + size < total) and (start + size <= 10000):
                    resp['next'] = _urlencode(processed_params,
                                              remove=rm_tup,
                                              insert=('start',
                                                      start + size))

        else:
            resp['message'] = "Something went wrong..."

        return resp

    def get_resource(self, collection, resource, fmt=None):

        def _generate_hierarchical_structure(string_list):
            # Takes a list of strings with possible '/' as hierarchical seperators
            # Returns a dict-structure with 'label', 'path' and possibly 'children'-keys

            def addHierItem(key, hierStruct, hierList, parent):
                if parent != "":
                    path = parent + "/" + key
                else:
                    path = key

                hierItem = {"label": key, "path": path}

                childrenList = []
                children = hierStruct.get(key)
                for childKey in sorted(children):
                    addHierItem(childKey, children, childrenList, path)

                if len(childrenList) > 0:
                    hierItem["children"] = childrenList

                hierList.append(hierItem)

            hierList = []
            hierStruct = {}
            for item in sorted(string_list):
                splitList = item.split("/")

                curLevel = hierStruct
                for key in splitList:
                    hierData = curLevel.get(key, {})
                    curLevel[key] = hierData
                    curLevel = hierData

            for key in sorted(hierStruct):
                addHierItem(key, hierStruct, hierList, "")

            return hierList

        def format_record(record):
            result = {}
            for key, value in record.items():
                # First handle all specialcases
                # If 'series' then treat uniquely
                if key == 'series':
                    output = []
                    currentLevel = []
                    urlpath = {}
                    collection = record.get('collection')

                    if collection:
                        urlpath['collection'] = collection.get('id')

                    for idx in value.split('/'):
                        currentLevel.append(idx)
                        urlpath['series'] = '/'.join(currentLevel)
                        level = {}
                        level['label'] = idx
                        level['new_link'] = self._generate_new_link(urlpath)
                        output.append(level)
                    result[key] = output

                # If key is list of strings
                elif key in ['admin_tags']:
                    output = []
                    for idx in value:
                        item = {}
                        item['label'] = idx
                        item['new_link'] = self._generate_new_link(key, idx)
                        output.append(item)
                    result[key] = output

                elif key in ['collection_tags']:
                    result[key] = _generate_hierarchical_structure(value)
                    
                elif key in ['resources']:
                    result[key] = value

                # If key is dict
                elif isinstance(value, dict) and key in self.filters:
                    # If id-dict
                    if value.get('id'):
                        _id = value.get('id')
                        label = value.get('label')
                        item = {}
                        item['label'] = label
                        item['id'] = _id
                        item['new_link'] = self._generate_new_link(key, _id)
                        result[key] = item
                    else:
                        result[key] = value

                # If key is list (of id-dicts)
                elif isinstance(value, list) and key in self.filters:
                    output = []

                    for _dict in value:

                        # hierarchical concept or entity
                        if isinstance(_dict.get('id'), list):
                            hierarchy = []
                            for i, v in enumerate(_dict.get('id')):
                                item = {}
                                item['id'] = v
                                item['label'] = _dict.get('label')[i]
                                item['new_link'] = '='.join([key, str(v)])
                                hierarchy.append(item)
                            output.append(hierarchy)

                        # flat concept or entity
                        else:
                            _id = _dict.get('id')
                            label = _dict.get('label')
                            item = {}
                            item['id'] = _id
                            item['label'] = label
                            item['new_link'] = self._generate_new_link(key, _id)
                            output.append(item)

                    result[key] = output

                else:
                    result[key] = value

            return result

        def format_collection(collection):

            # structure = collection.get('structure')
            # if structure:
            #     collection['structure'] = _generate_hierarchical_structure(structure)

            # Enhance with dynamically fetched structures from searchengine
            series, collection_tags = self.service.list_collection_structures(collection.get('id'))
            collection['series'] = series
            collection['collection_tags'] = collection_tags

            # Pop 'structure'-key - at least for now. Reintroduce when we can work with descriptions on
            # individual series-levels
            collection.pop('structure', None)

            # def addHierItem(key, hierStruct, hierList, parent):
            #     if parent != "":
            #         path = parent + "/" + key
            #     else:
            #         path = key

            #     hierItem = {"label": key, "path": path}

            #     childrenList = []
            #     children = hierStruct.get(key)
            #     for childKey in sorted(children):
            #         addHierItem(childKey, children, childrenList, path)

            #     if len(childrenList) > 0:
            #         hierItem["children"] = childrenList

            #     hierList.append(hierItem)

            # structure = collection.get('structure')
            # if structure:
            #     hierList = []
            #     hierStruct = {}
            #     for item in sorted(structure):
            #         splitList = item.split("/")

            #         curLevel = hierStruct
            #         for key in splitList:
            #             hierData = curLevel.get(key, {})
            #             curLevel[key] = hierData
            #             curLevel = hierData

            #     for key in sorted(hierStruct):
            #         addHierItem(key, hierStruct, hierList, "")

            #     collection['structure'] = hierList

            return collection

        response = self._get_request('/'.join([self.service_url,
                                               self.resources.get(collection),
                                               resource]))

        if response.get('status_code') == 0:
            res = response.get('result')
            if collection == 'records':
                if fmt == 'json':
                    return res
                else:
                    return format_record(res)
            elif collection == 'collections':
                return format_collection(res)
            else:
                return res

        elif response.get('status_code') == 1:
            return {
                'error': {
                    'code': 404,
                    'msg': 'Resourcen eksisterende ikke',
                    'id': resource
                }
            }
        elif response.get('status_code') == 2:
            return {
                'error': {
                    'code': 404,
                    'msg': 'Resourcen er slettet',
                    'id': resource
                }
            }
        else:
            return {
                'error': {
                    'code': response.get('status_code'),
                    'msg': response.get('status_msg'),
                    'id': resource
                }
            }

    def autocomplete(self, term, limit=10, domain=None):
        url = "https://aarhusiana.appspot.com/autocomplete_v3"
        params = [('t', term), ('limit', limit)]
        if domain and domain in ['events', 'people', 'organisations', 'locations', 'collections']:
            params.append(('domain', domain))
        response = requests.get(url, params=params)

        try:
            payload = json.loads(response.content)
            return payload.get('result')
        except ValueError as e:
            return {'status_code': 5, 'status_msg': e}

    def batch_records(self, id_list):
        if id_list:
            url = 'https://openaws.appspot.com/resolve_records_v2'
            data = {'view': 'record', 'oasid': json.dumps(id_list)}
            response = requests.post(url, data=data)
            try:
                payload = json.loads(response.content)
                if payload.get('status_code') == 0:
                    return payload.get('result')
            except ValueError as e:
                return {'status_code': 5, 'status_msg': e}
        else:
            return []

    def _generate_new_link(self, key, value=None):
        """Takes one dict of key(s) and value(s) OR two strings"""
        if value:
            # value = str(value) if isinstance(value, int) else value
            return self._urlencode_old({key: value})
        else:
            return self._urlencode_old(key)

    def _urlencode_old(self, params, decode=True):
        path = {}
        if type(params) == dict:
            iterable = params.items()
        else:
            iterable = params
        for key, value in iterable:

            if key in path:
                # path[key] += ';' + str(value).encode('utf-8')
                path[key] += ';' + str(value)
            else:
                # path[key] = str(value).encode('utf-8')
                path[key] = str(value)

        encoded = urllib.parse.urlencode(path)
        return encoded
        # if decode:
        #     return encoded.decode('utf-8')
        # else:
        #     return encoded

    def _get_request(self, url, params=None):
        response = requests.get(url, params=params)
        try:
            response_to_dict = json.loads(response.content)
            return response_to_dict
        except ValueError as e:
            return {'status_code': 5, 'error': e}

    ########################
    # DEPRECATED FUNCTIONS #
    ########################
    # PRIVATE GENERIC METHODS
    # def _urlencode(self, params=None, remove=None, insert=None):
    #     # params: list of tuples
    #     # insert: tuple
    #     # remove: tuple
    #     if params and remove and insert:
    #         out = [tup for tup in params + [insert] if tup != remove]
    #     elif params and remove:
    #         out = [tup for tup in params if tup != remove]
    #     elif params and insert:
    #         out = [tup for tup in params + [insert]]
    #     elif insert:
    #         out = [insert]
    #     elif params:
    #         out = params[:]
    #     else:
    #         return ""

    #     utf8_params = [(t[0], unicode(t[1]).encode('utf-8')) for t in out]
    #     return urllib.urlencode(utf8_params)

    # def list_facets(self):
    #     def _linkify_facets(facets):

    #         def generate_facet(facet_name, active_facets,):
    #             def _recursive(name, total_content,
    #                            active_facets):

    #                 for i in total_content:
    #                     _id = i.get('id')
    #                     current = (name, _id)
    #                     children = i.get('children')

    #                     if _id in active_facets:
    #                         i['count'] = active_facets.get(_id)
    #                         i['add_link'] = "=".join([name, _id])
    #                         if children:
    #                             _recursive(name, children, active_facets)

    #                 return total_content

    #             facet_label = self.facets[facet_name].get('label')
    #             total_content = self.facets[facet_name].get('content')
    #             linked_tree = _recursive(facet_name, total_content, active_facets)

    #             return {"label": facet_label, 'content': linked_tree}

    #         output = {}
    #         for facet_name in facets:
    #             # extract id and count from aws-output
    #             buckets = facets[facet_name].get('buckets')
    #             active_facets = {b.get('value'): b.get('count') for b in buckets}
    #             # generate links recursively
    #             output[facet_name] = generate_facet(facet_name, active_facets)

    #         return output

    #     resp = self.service.list_facets()
    #     return _linkify_facets(resp)

    # def get_resource(self, collection, resource, fmt=None):
    #     """Fetch a single resource.

    #     Args:
    #         collection (str): The domain to which the resource belongs.
    #         resource (str): The id of the resource.
    #         fmt (str): Defaults to None. Use 'json' to return JSON

    #     Returns:
    #         payload (dict)
    #     """
    #     def format_record(collection, resource):

    #         result = {}
    #         for key, value in resource.items():

    #             # First handle all specialcases
    #             # If 'series' then treat uniquely
    #             if key == 'series':
    #                 output = []
    #                 currentLevel = []
    #                 urlpath = {}

    #                 collection = resource.get('collection')
    #                 if collection:
    #                     urlpath['collection'] = collection.split(';')[0]

    #                 for idx in value.split('/'):
    #                     level = {}
    #                     currentLevel.append(idx)
    #                     urlpath['series'] = '/'.join(currentLevel)
    #                     level['label'] = idx
    #                     level['new_link'] = self._generate_new_link(urlpath)
    #                     output.append(level)
    #                 result[key] = output

    #             elif key in ['date_from', 'date_to']:
    #                 item = {}
    #                 item['label'] = key
    #                 item['date'] = value
    #                 item['new_link'] = self._generate_new_link(key, value)
    #                 result[key] = item

    #             # If key is list of simple FILTER-strings
    #             elif key in ['admin_tags', 'collection_tags', 'tags']:
    #                 output = []
    #                 for idx in value:
    #                     item = {}
    #                     item['label'] = idx
    #                     item['new_link'] = self._generate_new_link(key, idx)
    #                     output.append(item)
    #                 result[key] = output

    #             # If key is string
    #             elif isinstance(value, unicode):
    #                 # elif type(value) is unicode:
    #                 # If encoded string
    #                 if ';' in value:
    #                     _id = value.split(';')[0]
    #                     item = {}
    #                     item['id'] = _id
    #                     item['label'] = value.split(';')[1]
    #                     item['new_link'] = self._generate_new_link(key, _id)
    #                     result[key] = item
    #                 # Else simple string
    #                 else:
    #                     result[key] = value

    #             # If key is list of encoded strings
    #             elif isinstance(value, list):
    #                 # elif type(value) == list:
    #                 output = []
    #                 for idx in value:
    #                     if ';' in idx:
    #                         _id = idx.split(';')[0]
    #                         item = {}
    #                         item['id'] = _id
    #                         item['label'] = idx.split(';')[1]
    #                         item['new_link'] = self._generate_new_link(key, _id)
    #                         output.append(item)
    #                     else:
    #                         output.append(idx)
    #                 result[key] = output

    #             else:
    #                 result[key] = value

    #         return result

    #     # response = self.service.get_resource(collection, resource)
    #     response = self._get_request('/'.join([self.service_url,
    #                                            self.resources.get(collection),
    #                                            resource]))
    #     if response.get('status_code') == 0:
    #         # If json-view, no need to process GUI-stuff
    #         # jsonify() will convert the dict back to json
    #         if fmt == 'json':
    #             return response
    #         else:
    #             return format_record(collection, response.get('result'))
    #     else:
    #         return response

    # def archived_functions(self):

    #     def _generate_filters(filter_list, params):
    #         # Takes filters-array of filters and adds view- and remove-links
    #         filters = deepcopy(filter_list)
    #         for f in filters:
    #             key = f.get('key')
    #             value = f.get('value')
    #             if f.get('label'):
    #                 f['view_link'] = "/".join([key, value])

    #             if key == 'collection':
    #                 new_params = [(k, v) for k, v in params if k != (key or 'series')]
    #                 f['remove_link'] = _urlencode(new_params)
    #             else:
    #                 f['remove_link'] = _urlencode(params, remove=(key, value))

    #         return filters

    #     def _generate_facets(params, server_facets):

    #         def _generate_facet(name, counts, params=None):

    #             def recursive(name, tree, counts, params=None):

    #                 for item in tree:
    #                     _id = item.get('id')
    #                     current = (name, _id)
    #                     children = item.get('children')

    #                     if counts and (_id in counts):
    #                         item['count'] = counts.get(_id)

    #                         if params and (current in params):
    #                             item['remove_link'] = _urlencode(params, remove=current)
    #                         elif params:
    #                             item['add_link'] = _urlencode(params, insert=current)

    #                     if children:
    #                         recursive(name, children, counts, params)

    #                 return tree

    #             label = FACETS[name].get('label')
    #             tree = FACETS[name].get('content')
    #             linked_tree = recursive(name, tree, counts, params)

    #             return {"label": label, 'content': linked_tree}

    #         output = {}
    #         facets = deepcopy(server_facets)
    #         for name in facets:
    #             buckets = facets[name].get('buckets')
    #             counts = {b.get('value'): b.get('count') for b in buckets}
    #             output[name] = _generate_facet(name, counts, params)

    #         return output
