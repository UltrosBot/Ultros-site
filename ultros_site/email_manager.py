# coding=utf-8
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from mako.lookup import TemplateLookup
from mako.template import Template
from ruamel import yaml

__author__ = "Gareth Coles"


class EmailManager:
    def __init__(self):
        with open("config.yml", "r") as fh:
            self.config = yaml.safe_load(fh)["email"]

        ssl = self.config["ssl"]

        if ssl is True:
            self._connection = self._connection_ssl
        elif ssl is False:
            self._connection = self._connection_plain
        elif str(ssl).lower() == "starttls":
            self._connection = self._connection_starttls
        else:
            raise RuntimeError(
                "Unknown SSL mode '{}' - must be True, False or 'startssl'.".format(ssl)
            )

        self.template_lookup = TemplateLookup(["./templates/email/"])

    def send_email(self, template, recipient, subject, **kwargs):
        plain_template = self.render_template(
            "plain/{}.txt".format(template), **kwargs
        )

        html_template = self.render_template(
            "html/{}.html".format(template), **kwargs
        )

        message = MIMEMultipart("alternative")

        message["Subject"] = subject
        message["From"] = self.config["from"]
        message["To"] = recipient

        message.attach(MIMEText(plain_template, "plain"))
        message.attach(MIMEText(html_template, "html"))

        connection = self.get_connection()
        connection.sendmail(self.config["from"], recipient, message.as_string())
        connection.quit()

    def get_connection(self):
        connection = self._connection()

        user = self.config.get("user")

        if user:
            connection.login(user, self.config["password"])

        return connection

    def _connection_plain(self):
        connection = smtplib.SMTP(
            host=self.config["host"],
            port=self.config["port"]
        )

        connection.ehlo()

        return connection

    def _connection_ssl(self):
        connection = smtplib.SMTP_SSL(
            host=self.config["host"],
            port=self.config["port"]
        )

        connection.ehlo()

        return connection

    def _connection_starttls(self):
        connection = smtplib.SMTP(
            host=self.config["host"],
            port=self.config["port"]
        )

        connection.ehlo()
        connection.starttls()

        return connection

    def get_template(self, uri) -> Template:
        return self.template_lookup.get_template(uri)

    def render_template(self, uri, *args, **kwargs):
        return self.get_template(uri).render(*args, **kwargs)

    @property
    def enabled(self):
        return self.config["use"]
