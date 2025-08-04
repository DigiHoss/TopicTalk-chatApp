def init_config(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///TopicTalk.db"
    app.config['SECRET_KEY'] = 'a7f8c2d1e49b4e6fa935b1c019da764b'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'topictalk.contact@gmail.com'
    app.config['MAIL_PASSWORD'] = 'zajltzvdkmxnndtj'  # mdp : TopicTalk1234
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True

    