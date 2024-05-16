class Config:
    SECRET_KEY = 'cae40d308a9c0bbf29b12ce29adc93b2'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER ="smtp.qq.com"
    MAIL_USE_SSL = True
    MAIL_PORT = 465
    MAIL_USERNAME ="2849115967@qq.com"
    MAIL_PASSWORD ="uqlbhymhdmrkddgg"
    MAIL_DEFAULT_SENDER ="2849115967@qq.com"

    WTF_CSRF_ENABLED = False