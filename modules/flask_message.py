from flask import render_template


class FlaskMessage:
    @staticmethod
    def get(title, content, url):
        return render_template('message.html', title=title, content=content,url=url)