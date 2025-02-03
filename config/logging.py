from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'simple': {
            'format': '{levelname} | {asctime:s} | {name} | {message}',
            'style': '{'
        },
        'verbose': {
            'format': '{levelname} | {asctime:s} | {name} | '
                      '{module}.py (line {lineno:d}) | {funcName} | {message}',
            'style': '{'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': BASE_DIR / 'logs/django_debug.log'
        },
        'file_ingredient_ai': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': BASE_DIR / 'logs/ingredient_ai_info.log'
        },
        'mail_admins': {
            'level': 'WARNING',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'verbose',
            'filters': ['require_debug_false'],
            'include_html': True
        }
    },
    'loggers': {
        '': {
            'level': 'WARNING',
            'handlers': ['console', 'file']
        },
        'django': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': False
        },
        'ingredient_ai': {
            'level': 'INFO',
            'handlers': ['console', 'file_ingredient_ai'],
            'propagate': False
        },
        'django.template': {
            'level': 'DEBUG',
            'handlers': ['file'],
            'propagate': False
        }
    }
}
