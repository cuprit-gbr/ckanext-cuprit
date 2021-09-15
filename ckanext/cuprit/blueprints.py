from flask import render_template

def render_about_custom_page():
    u'''A simple template with a helper that exists. Rendering with a helper
    shouldn't raise an exception.'''

    return render_template('participate.html')