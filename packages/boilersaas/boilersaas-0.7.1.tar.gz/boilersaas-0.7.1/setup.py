from setuptools import setup, find_packages

setup(
    name="boilersaas",
    version="0.7.1",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
      package_data={
        # Include templates, translations, and any other non-python files
      "boilersaas": [
            "templates/**/*.html",  # Recursively include all HTML files in templates directory
            "translations/**/*",  # Recursively include all files in translations directory
        ],
      },
    install_requires=[
        "Babel>=2.14.0",
        "Flask>=3.0.2",
        "flask-babel>=4.0.0",
        "Flask-Dance>=7.1.0",
        "Flask-Login>=0.6.3",
        "Flask-Mail>=0.9.1",
        "Flask-SQLAlchemy>=3.1.1",
        "Flask-WTF>=1.2.1",
        "itsdangerous>=2.1.2",
        "python-dotenv>=1.0.1",
        "requests>=2.31.0",
        "SQLAlchemy>=2.0.28",
        "Werkzeug>=3.0.1",
        "WTForms>=3.1.2",
        "email_validator>=2.1.1" # WFForms dependency, not included in Flask-WTF
    ],
    author="DS",
    author_email="hello@davidstern.me",
    description="A boilerplate for flask SAAS apps, with social sign in, email confirmation, and more.",
    keywords="flask,boilerplate,saas,app",
    url="http://example.com/your_package",  # Optional
)
